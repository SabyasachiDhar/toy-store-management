import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  fetchInvoices,
  createInvoice,
  updateInvoice,
  deleteInvoice,
} from '../../store/slices/invoicesSlice';
import styles from './Invoices.module.css';

const Invoices = () => {
  const dispatch = useDispatch();
  const { items, loading, error } = useSelector((state) => state.invoices);
  const [formData, setFormData] = useState({
    customer_id: '',
    invoice_number: '',
    total_amount: '',
    status: 'pending',
  });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    dispatch(fetchInvoices());
  }, [dispatch]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (editingId) {
      dispatch(updateInvoice({ id: editingId, data: formData }));
      setEditingId(null);
    } else {
      dispatch(createInvoice(formData));
    }
    setFormData({
      customer_id: '',
      invoice_number: '',
      total_amount: '',
      status: 'pending',
    });
  };

  const handleEdit = (invoice) => {
    setEditingId(invoice.id);
    setFormData({
      customer_id: invoice.customer_id,
      invoice_number: invoice.invoice_number,
      total_amount: invoice.total_amount,
      status: invoice.status,
    });
  };

  const handleDelete = (id) => {
    dispatch(deleteInvoice(id));
  };

  return (
    <div className={styles.container}>
      <h2>Invoices Management</h2>

      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.formRow}>
          <div className={styles.formGroup}>
            <label htmlFor="customer_id">Customer ID:</label>
            <input
              type="number"
              id="customer_id"
              name="customer_id"
              value={formData.customer_id}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="invoice_number">Invoice Number:</label>
            <input
              type="text"
              id="invoice_number"
              name="invoice_number"
              value={formData.invoice_number}
              onChange={handleInputChange}
              required
            />
          </div>
        </div>

        <div className={styles.formRow}>
          <div className={styles.formGroup}>
            <label htmlFor="total_amount">Total Amount:</label>
            <input
              type="number"
              id="total_amount"
              name="total_amount"
              step="0.01"
              value={formData.total_amount}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="status">Status:</label>
            <select
              id="status"
              name="status"
              value={formData.status}
              onChange={handleInputChange}
            >
              <option value="pending">Pending</option>
              <option value="paid">Paid</option>
              <option value="overdue">Overdue</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>
        </div>

        <button type="submit" className={styles.button}>
          {editingId ? 'Update Invoice' : 'Add Invoice'}
        </button>
        {editingId && (
          <button
            type="button"
            onClick={() => {
              setEditingId(null);
              setFormData({
                customer_id: '',
                invoice_number: '',
                total_amount: '',
                status: 'pending',
              });
            }}
            className={styles.cancelBtn}
          >
            Cancel
          </button>
        )}
      </form>

      {error && <div className={styles.error}>{error}</div>}
      {loading && <div className={styles.loading}>Loading...</div>}

      <div className={styles.tableContainer}>
        <table className={styles.table}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Customer ID</th>
              <th>Invoice Number</th>
              <th>Amount</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {items && Array.isArray(items) ? items.map((invoice) => (
              <tr key={invoice.id}>
                <td>{invoice.id}</td>
                <td>{invoice.customer_id}</td>
                <td>{invoice.invoice_number}</td>
                <td>${parseFloat(invoice.total_amount).toFixed(2)}</td>
                <td>
                  <span className={`${styles.status} ${styles[invoice.status]}`}>
                    {invoice.status}
                  </span>
                </td>
                <td>
                  <button
                    onClick={() => handleEdit(invoice)}
                    className={styles.editBtn}
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(invoice.id)}
                    className={styles.deleteBtn}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            )) : null}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Invoices;
