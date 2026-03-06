import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { invoicesAPI } from '../../services/api';

export const fetchInvoices = createAsyncThunk(
  'invoices/fetchInvoices',
  async (_, { rejectWithValue }) => {
    try {
      const response = await invoicesAPI.getAll();
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Error fetching invoices');
    }
  }
);

export const createInvoice = createAsyncThunk(
  'invoices/createInvoice',
  async (invoiceData, { rejectWithValue }) => {
    try {
      const response = await invoicesAPI.create(invoiceData);
      return response.data.invoice || response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Error creating invoice');
    }
  }
);

export const updateInvoice = createAsyncThunk(
  'invoices/updateInvoice',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const response = await invoicesAPI.update(id, data);
      return response.data.invoice || response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Error updating invoice');
    }
  }
);

export const deleteInvoice = createAsyncThunk(
  'invoices/deleteInvoice',
  async (id, { rejectWithValue }) => {
    try {
      await invoicesAPI.delete(id);
      return id;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Error deleting invoice');
    }
  }
);

const initialState = {
  items: [],
  loading: false,
  error: null,
};

const invoicesSlice = createSlice({
  name: 'invoices',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchInvoices.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchInvoices.fulfilled, (state, action) => {
        state.loading = false;
        if (Array.isArray(action.payload)) {
          state.items = action.payload;
        } else if (Array.isArray(action.payload?.invoices)) {
          state.items = action.payload.invoices;
        } else if (Array.isArray(action.payload?.data)) {
          state.items = action.payload.data;
        } else {
          state.items = [];
        }
      })
      .addCase(fetchInvoices.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(createInvoice.fulfilled, (state, action) => {
        if (Array.isArray(state.items)) {
          state.items.push(action.payload);
        }
      })
      .addCase(updateInvoice.fulfilled, (state, action) => {
        if (Array.isArray(state.items)) {
          const index = state.items.findIndex((item) => item.id === action.payload.id);
          if (index !== -1) {
            state.items[index] = action.payload;
          }
        }
      })
      .addCase(deleteInvoice.fulfilled, (state, action) => {
        if (Array.isArray(state.items)) {
          state.items = state.items.filter((item) => item.id !== action.payload);
        }
      });
  },
});

export default invoicesSlice.reducer;
