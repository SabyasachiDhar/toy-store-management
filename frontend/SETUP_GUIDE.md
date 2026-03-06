# Toy Store Management Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure Environment (Optional)
Copy `.env.example` to `.env.local`:
```bash
cp .env.example .env.local
```

Update the API base URL if your backend runs on a different port:
```
REACT_APP_API_BASE_URL=http://localhost:5000/api
```

### 3. Start Development Server
```bash
npm start
```

Application opens at `http://localhost:3000`

### 4. Build for Production
```bash
npm run build
```

## Features Included

✅ **Dashboard** - Real-time statistics and analytics
✅ **Customers Management** - Full CRUD operations
✅ **Products Management** - Inventory management
✅ **Invoices Management** - Invoice tracking with status
✅ **Redux Toolkit** - Centralized state management
✅ **Axios** - HTTP client for API calls
✅ **Responsive Design** - Mobile-friendly UI
✅ **Error Handling** - User-friendly error messages
✅ **Loading States** - Visual feedback during API calls

## API Integration

The app connects to the following endpoints:

| Module | Endpoint |
|--------|----------|
| Customers | `/api/customers` |
| Products | `/api/products` |
| Invoices | `/api/invoices` |

## Backend Requirements

Ensure your backend API:
- Runs on `http://localhost:5000`
- Has CORS enabled for `http://localhost:3000`
- Supports JSON responses
- Implements all three endpoints mentioned above

## Project Structure

```
src/
├── components/     # React components
├── store/          # Redux store configuration
├── services/       # API client with Axios
├── App.js          # Main component
└── index.js        # Entry point
```

## Key Technologies

- React 18.2
- Redux Toolkit
- Axios
- CSS Modules
- React Scripts

## Troubleshooting

### CORS Error
Make sure your backend has CORS configured properly.

### API Connection Error
Verify the `API_BASE_URL` in `src/services/api.js` matches your backend URL.

### Port Already in Use
If port 3000 is in use, React will prompt to use another port.

## Development

### ESP: Using Redux DevTools
Install Redux DevTools browser extension for better debugging.

### CSS Customization
Each component has its own CSS module. Modify component-specific styles in the respective `.module.css` files.

## Production Deployment

1. Build the project:
   ```bash
   npm run build
   ```

2. Serve the `build` directory:
   - Using a static web server
   - Deploy to Vercel, Netlify, or similar platforms
   - Update the `API_BASE_URL` in `src/services/api.js` to your production backend URL

## Support

For issues, refer to:
- React documentation: https://react.dev
- Redux Toolkit docs: https://redux-toolkit.js.org
- Axios docs: https://axios-http.com
