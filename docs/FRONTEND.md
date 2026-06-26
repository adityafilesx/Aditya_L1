# Frontend Architecture

## Stack
- **Framework:** React 19 + TypeScript
- **Build Tool:** Vite 6
- **Routing:** React Router 7
- **Styling:** Tailwind CSS + Custom CSS Variables
- **3D Visualization:** Three.js
- **State Management:** React Context (Future: Redux or Zustand if needed)

## Folder Structure
- `src/features/` - Domain-specific React components (e.g., PhysicsLab, MissionControl).
- `src/styles/` - Design system, theming, and accessibility utilities.
- `src/services/` - API interaction layer (Phase FE-5).
- `src/shared/` - Common UI components like Buttons, Cards, Layouts.

## Execution
To run the frontend independently:
```bash
cd frontend/
npm install
npm run dev
```
