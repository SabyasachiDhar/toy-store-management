import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { productsAPI } from '../../services/api';

export const fetchProducts = createAsyncThunk(
  'products/fetchProducts',
  async (_, { rejectWithValue }) => {
    try {
      const response = await productsAPI.getAll();
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Error fetching products');
    }
  }
);

export const createProduct = createAsyncThunk(
  'products/createProduct',
  async (productData, { rejectWithValue }) => {
    try {
      const response = await productsAPI.create(productData);
      return response.data.product || response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Error creating product');
    }
  }
);

export const updateProduct = createAsyncThunk(
  'products/updateProduct',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const response = await productsAPI.update(id, data);
      return response.data.product || response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Error updating product');
    }
  }
);

export const deleteProduct = createAsyncThunk(
  'products/deleteProduct',
  async (id, { rejectWithValue }) => {
    try {
      await productsAPI.delete(id);
      return id;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Error deleting product');
    }
  }
);

const initialState = {
  items: [],
  loading: false,
  error: null,
};

const productsSlice = createSlice({
  name: 'products',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchProducts.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchProducts.fulfilled, (state, action) => {
        state.loading = false;
        if (Array.isArray(action.payload)) {
          state.items = action.payload;
        } else if (Array.isArray(action.payload?.products)) {
          state.items = action.payload.products;
        } else if (Array.isArray(action.payload?.data)) {
          state.items = action.payload.data;
        } else {
          state.items = [];
        }
      })
      .addCase(fetchProducts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(createProduct.fulfilled, (state, action) => {
        if (Array.isArray(state.items)) {
          state.items.push(action.payload);
        }
      })
      .addCase(updateProduct.fulfilled, (state, action) => {
        if (Array.isArray(state.items)) {
          const index = state.items.findIndex((item) => item.id === action.payload.id);
          if (index !== -1) {
            state.items[index] = action.payload;
          }
        }
      })
      .addCase(deleteProduct.fulfilled, (state, action) => {
        if (Array.isArray(state.items)) {
          state.items = state.items.filter((item) => item.id !== action.payload);
        }
      });
  },
});

export default productsSlice.reducer;
