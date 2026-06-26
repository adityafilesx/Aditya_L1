# Scientific Asset Manager

## Purpose
The `backend/data/processed/spectral_fitting_images` repository generates hundreds of static correlation charts, histograms, and flare evolution frames. The **Asset Manager** acts as the frontend gallery to explore, filter, and organize these artifacts contextually.

## Component: `AssetManagerPage.tsx`
- **Location**: `frontend/src/features/knowledge-graph/AssetManagerPage.tsx`
- **Routing**: Available under the `/knowledge/assets` route via the primary sidebar.

## Core Features
1. **Search & Filter**: Allows operators to query active regions (e.g., `AR13872`), event classifications (`X2.2`), or image types (`Hardness Ratio`).
2. **Metadata Tagging**: Each image renders with parsed contextual metadata:
   - Event ID
   - Timestamp (ISO 8601)
   - Active Region Target
   - Metric Classification
3. **Actions**: Bookmarking or direct download functionality for report generation or Jupyter notebook exports.

## Future Hooks
- Click-to-overlay: Fetching an asset could trigger `workspaceStore.setCursorTime` and `workspaceStore.setActiveRegion` automatically, snapping the Digital Twin viewer back to the exact historical moment the image was generated.
