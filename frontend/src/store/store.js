import { configureStore } from '@reduxjs/toolkit';
import customersReducer from './slices/customersSlice';
import productsReducer from './slices/productsSlice';
import invoicesReducer from './slices/invoicesSlice';

const store = configureStore({
  reducer: {
    customers: customersReducer,
    products: productsReducer,
    invoices: invoicesReducer,
  },
});

export default store;
