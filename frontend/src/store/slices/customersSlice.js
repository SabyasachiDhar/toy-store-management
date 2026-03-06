import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { customersAPI } from '../../services/api';

export const fetchCustomers = createAsyncThunk(
  'customers/fetchCustomers',
  async (_, { rejectWithValue }) => {
    try {
      const response = await customersAPI.getAll();
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Error fetching customers');
    }
  }
);

export const createCustomer = createAsyncThunk(
  'customers/createCustomer',
  async (customerData, { rejectWithValue }) => {
    try {
      const response = await customersAPI.create(customerData);
      return response.data.customer || response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Error creating customer');
    }
  }
);

export const updateCustomer = createAsyncThunk(
  'customers/updateCustomer',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const response = await customersAPI.update(id, data);
      return response.data.customer || response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Error updating customer');
    }
  }
);

export const deleteCustomer = createAsyncThunk(
  'customers/deleteCustomer',
  async (id, { rejectWithValue }) => {
    try {
      await customersAPI.delete(id);
      return id;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Error deleting customer');
    }
  }
);

const initialState = {
  items: [],
  loading: false,
  error: null,
};

const customersSlice = createSlice({
  name: 'customers',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchCustomers.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchCustomers.fulfilled, (state, action) => {
        state.loading = false;
        if (Array.isArray(action.payload)) {
          state.items = action.payload;
        } else if (Array.isArray(action.payload?.customers)) {
          state.items = action.payload.customers;
        } else if (Array.isArray(action.payload?.data)) {
          state.items = action.payload.data;
        } else {
          state.items = [];
        }
      })
      .addCase(fetchCustomers.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(createCustomer.fulfilled, (state, action) => {
        if (Array.isArray(state.items)) {
          state.items.push(action.payload);
        }
      })
      .addCase(updateCustomer.fulfilled, (state, action) => {
        if (Array.isArray(state.items)) {
          const index = state.items.findIndex((item) => item.id === action.payload.id);
          if (index !== -1) {
            state.items[index] = action.payload;
          }
        }
      })
      .addCase(deleteCustomer.fulfilled, (state, action) => {
        if (Array.isArray(state.items)) {
          state.items = state.items.filter((item) => item.id !== action.payload);
        }
      });
  },
});

export default customersSlice.reducer;
