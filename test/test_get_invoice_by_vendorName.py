import unittest
from db_util import init_db, clean_db , save_inv_extraction
from fastapi.testclient import TestClient
from app import app


class TestGetInvoicesByVendorName(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        init_db()

        self.vendor_name = "SuperStore"

        invoice_1 = {
            "InvoiceId": 1,
            "VendorName": self.vendor_name,
            "Items": [
                {
                    "Description": "Pen",
                    "Name": "Blue Pen",
                    "Quantity": 2,
                    "UnitPrice": 5.0,
                    "Amount": 10.0
                }
            ]
        }

        invoice_2 = {
            "InvoiceId": 2,
            "VendorName": self.vendor_name,
            "Items": [
                {
                    "Description": "Pen1",
                    "Name": "Blue Pen1",
                    "Quantity": 3,
                    "UnitPrice": 37.0,
                    "Amount": 111.0
                }
            ]
        }

        # Seed invoice 1
        save_inv_extraction({"data": invoice_1})

        # Seed invoice 2
        save_inv_extraction({"data": invoice_2})


    def test_invoice_by_vendor_found(self):
        # Act: call the endpoint with the seeded invoice vendor name
        response = self.client.get(f"/invoices/vendor/{self.vendor_name}")
        self.assertEqual(response.status_code, 200)
        # Assert: response JSON structure
        data = response.json()
        self.assertIsInstance(data, dict)
        # Assert : Vendor name is the same
        self.assertEqual(data["VendorName"],self.vendor_name)
        # Assert : Numbers of the invoices is 2
        self.assertEqual(data["TotalInvoices"],2)
        # Assert: Invoices exists and is a non-empty list
        self.assertIn("invoices", data)
        self.assertIsInstance(data["invoices"], list)
        self.assertEqual(len(data["invoices"]),2)
        

    def test_invoice_not_found_vendor(self):
        invalid_Vendor_name = "Super"
        response = self.client.get(f"/invoices/vendor/{invalid_Vendor_name}")
        # Assert: status code 
        self.assertEqual(response.status_code,200)
        # Assert: response JSON structure
        data=response.json()
        self.assertEqual(data["VendorName"], "Unknown Vendor")
        self.assertEqual(data["TotalInvoices"], 0)
        self.assertIsInstance(data["invoices"], list)
        self.assertEqual(len(data["invoices"]),0)
        
    def tearDown(self):
        clean_db() 
"""
from fastapi.testclient import TestClient
from unittest.mock import patch

from app import app  # אם הקובץ שלך לא נקרא app.py תשני בהתאם

client = TestClient(app)


def test_get_invoices_by_vendor_returns_invoices():
    vendor_name = "Amazon"

    mocked_invoices = [
        {
            "InvoiceId": "INV-1",
            "VendorName": "Amazon",
            "InvoiceDate": "2025-01-01T00:00:00+00:00",
            "SubTotal": 100.0,
            "ShippingCost": 10.0,
            "InvoiceTotal": 110.0
        },
        {
            "InvoiceId": "INV-2",
            "VendorName": "Amazon",
            "InvoiceDate": "2025-01-02T00:00:00+00:00",
            "SubTotal": 50.0,
            "ShippingCost": 0.0,
            "InvoiceTotal": 50.0
        }
    ]

    with patch("app.db_util.get_invoices_by_vendor", return_value=mocked_invoices) as mock_fn:
        res = client.get(f"/invoices/vendor/{vendor_name}")

    assert res.status_code == 200
    body = res.json()

    assert body["VendorName"] == vendor_name
    assert body["TotalInvoices"] == 2
    assert body["invoices"] == mocked_invoices

    mock_fn.assert_called_once_with(vendor_name)


def test_get_invoices_by_vendor_returns_unknown_vendor_when_empty():
    vendor_name = "NoSuchVendor"

    with patch("app.db_util.get_invoices_by_vendor", return_value=[]) as mock_fn:
        res = client.get(f"/invoices/vendor/{vendor_name}")

    assert res.status_code == 200
    body = res.json()

    assert body["VendorName"] == "Unknown Vendor"
    assert body["TotalInvoices"] == 0
    assert body["invoices"] == []

    mock_fn.assert_called_once_with(vendor_name)
"""