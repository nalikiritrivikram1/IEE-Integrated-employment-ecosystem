# IEE Integrated Employment Ecosystem

Backend-enabled government employment portal based on the original `iee_government_portal.html` UI, with the frontend theme kept intact and the portal features connected to a local Python backend.

## Repository

- GitHub: [nalikiritrivikram1/IEE-Integrated-employment-ecosystem](https://github.com/nalikiritrivikram1/IEE-Integrated-employment-ecosystem)

## Live Preview

- Local live preview: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

This project currently runs as a local backend server, so the preview link works after starting the app on the same machine.

## Included Files

- `app.py`: Python backend server that injects backend-powered behavior into the portal
- `iee_government_portal.html`: original portal frontend kept in the repo
- `portal_data.json`: seeded local backend data store
- `docs/iee-comprehensive-audit-roadmap.md`: decision-ready audit, benchmark matrix, and implementation roadmap
- `.gitignore`: ignores runtime-only files

## Audit and Roadmap

- See `docs/iee-comprehensive-audit-roadmap.md` for the current product audit, production blockers, benchmark review, phased roadmap, and target API/domain model.

## Backend Features Added

- Worker login, registration, worker ID generation, verification, job applications
- Employer login, single job posting, bulk hiring, direct worker hiring
- Verifier login, queue actions, field KYC processing, QR-related actions
- Super admin hidden login, user actions, verifier creation, notice publishing
- Dashboard sidebar modules for worker, employer, verifier, and super admin portals
- Persistent local data storage with safer atomic JSON writes

## Run Locally

1. Open the project folder.
2. Run:

```powershell
python app.py
```

3. Open:

```text
http://127.0.0.1:8000/
```

## Notes

- The portal frontend/theme was intentionally not changed.
- The hidden admin access is still available in the portal.
- Super admin shortcut: `Ctrl + Shift + Alt + A`

## Render Deployment

- Build Command: leave empty
- Start Command: `python app.py`

This app is now configured for Render and will:

- load `iee_government_portal.html` from the repository itself
- bind to `0.0.0.0`
- use Render's `PORT` environment variable automatically
