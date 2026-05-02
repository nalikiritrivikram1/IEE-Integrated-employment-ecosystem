const { chromium } = require('playwright');

(async () => {
  const target = 'http://127.0.0.1:8000/';
  const browser = await chromium.launch({
    headless: true,
    channel: 'chrome',
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1200 } });
  const errors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  page.on('console', (msg) => {
    if (msg.type() === 'error' && !msg.text().includes('Failed to load resource')) errors.push(msg.text());
  });

  await page.goto(target);
  const navText = await page.locator('.mainnav').innerText();
  if (navText.includes('Live Services')) {
    throw new Error('Separate Live Services nav is still visible');
  }
  if (await page.locator('#live-features-page').count()) {
    throw new Error('Separate Live Services page still exists');
  }
  await page.locator('.mainnav .nl', { hasText: 'Worker Portal' }).click();
  await page.locator('#w-id-inp').fill('9876500010');
  await page.locator('#w-pw-inp').fill('Worker@001');
  await page.getByText('Login as Worker').click();
  await page.waitForSelector('#worker-page.show');
  await page.getByText('Personalised Job Alerts').click();
  await page.getByText('Generate Live Result').click();
  await page.waitForSelector('#lf-output .badge.b-gray');
  const modalOutput = await page.locator('#lf-output').innerText();
  const workerTools = await page.locator('#worker-page .smart-tools').innerText();
  const employerLinkText = await page.locator('#employer-page .dmenu').innerText();
  await page.screenshot({ path: 'portal-live-services-preview.png', fullPage: true });
  await browser.close();

  console.log(JSON.stringify({
    navText,
    modalOutput: modalOutput.slice(0, 180),
    workerTools: workerTools.slice(0, 180),
    employerLinkText: employerLinkText.slice(0, 120),
    errors,
    screenshot: 'portal-live-services-preview.png',
  }, null, 2));

  if (!modalOutput.includes('Backend persisted') || !modalOutput.includes('Personalised alerts generated') || !workerTools.includes('NPS-Lite Pension') || employerLinkText.includes('Live Services') || errors.length) {
    process.exit(1);
  }
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
