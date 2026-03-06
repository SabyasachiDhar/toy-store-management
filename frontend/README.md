# Toy Store Management Frontend

A modern React 18.2 application for managing toy store inventory, customers, and invoices using Redux Toolkit and Axios.

## Features

- **Dashboard**: Real-time statistics and analytics
- **Customers Management**: Create, read, update, and delete customers
- **Products Management**: Manage toy store inventory with pricing
- **Invoices Management**: Track customer invoices with different status states
- **Redux State Management**: Centralized state using Redux Toolkit
- **API Integration**: Axios-based HTTP client for backend integration
- **Responsive Design**: Mobile-friendly UI with CSS modules

## Tech Stack

- **React 18.2**: Latest React version
- **Redux Toolkit**: State management
- **Axios**: HTTP client
- **CSS Modules**: Component-scoped styling
- **React Scripts**: Build tool

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Navigation/
│   │   ├── Dashboard/
│   │   ├── Customers/
│   │   ├── Products/
│   │   └── Invoices/
│   ├── services/
│   │   └── api.js
│   ├── store/
│   │   ├── store.js
│   │   └── slices/
│   │       ├── customersSlice.js
│   │       ├── productsSlice.js
│   │       └── invoicesSlice.js
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

## Installation

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Update the API base URL in `src/services/api.js` if needed:
   ```javascript
   const API_BASE_URL = 'http://localhost:5000/api';
   ```

## Running the Application

### Development Mode

```bash
npm start
```

The application will open at `http://localhost:3000`

### Build for Production

```bash
npm build
```

### Run Tests

```bash
npm test
```

## API Endpoints

The application connects to the backend API with the following endpoints:

- **Customers**: `/api/customers`
- **Products**: `/api/products`
- **Invoices**: `/api/invoices`

### Expected Backend Response Format

```json
{
  "endpoints": {
    "customers": "/api/customers",
    "invoices": "/api/invoices",
    "products": "/api/products"
  },
  "message": "Inventory Management API",
  "version": "1.0.0"
}
```

## Components

### Dashboard
- Displays overall statistics and system information
- Shows inventory value, invoice status, and product metrics

### Customers
- CRUD operations for customer management
- Fields: Name, Email, Phone
- Form validation and error handling

### Products
- Manage toy store inventory
- Fields: Name, Description, Price, Quantity
- Real-time inventory calculations

### Invoices
- Track customer invoices
- Status management (Pending, Paid, Overdue, Cancelled)
- Links to customer information

## State Management (Redux)

### Slices

1. **customersSlice**: Manages customer state
2. **productsSlice**: Manages product inventory
3. **invoicesSlice**: Manages invoice data

Each slice includes:
- Async thunks for API calls
- State for items, loading, and error
- Extra reducers for handling async actions

## Styling

The application uses CSS Modules for component-level styling with:
- Responsive grid layouts
- Mobile-first design
- Color-coded status indicators
- Smooth transitions and hover effects

## Error Handling

- Network error handling with user-friendly messages
- Loading states during API calls
- Form validation before submission

## CORS Configuration

Ensure your backend API has CORS enabled to accept requests from `http://localhost:3000`

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT License - Feel free to use this project for educational and commercial purposes.

## Support

For issues or questions, please create an issue in the repository or contact the development team.
