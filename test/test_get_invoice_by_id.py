import unittest
from db_util import init_db, clean_db , save_inv_extraction
from fastapi.testclient import TestClient
from app import app

class TestGetInvoiceById(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        init_db()

        self.invoice_id = 2910
        self.vendor_name = "SuperStore"

        SEED_DATA = {
            "InvoiceId" : self.invoice_id,
            "VendorName" : self.vendor_name,
            "Items" : [ 
                {
                    "Description": "Pen",
                    "Name": "Blue Pen",
                    "Quantity": 2,
                    "UnitPrice": 5.0,
                    "Amount": 10.0
                }
            ]
        }

        result = {"data": SEED_DATA}
        save_inv_extraction(result)

    def test_invoice_found(self):
        # Act: call the endpoint with the seeded invoice id
        response = self.client.get(f"/invoice/{self.invoice_id}")

        # Assert: status code first
        self.assertEqual(response.status_code, 200)

        # Assert: response JSON structure
        data = response.json()
        self.assertIsInstance(data, dict)
        
        #Asser : ID is the same
        self.assertEqual(data["InvoiceId"],str(self.invoice_id))

        # Assert: Items exists and is a non-empty list
        self.assertIn("Items", data)
        items = data["Items"]
        self.assertIsInstance(items, list)
        self.assertGreater(len(items), 0)
        

    def test_invoice_not_found(self):
        invalid_id = 999999
        response = self.client.get(f"/invoice/{invalid_id}")
        # Assert: status code 
        self.assertEqual(response.status_code,404)
        # Assert: response JSON structure
        self.assertEqual(response.json(), {"detail": "Invoice not found"})
        

    def tearDown(self):
        clean_db() 




"""

import unittest
from unittest.mock import patch 
import app
from db_util import init_db
from fastapi.testclient import TestClient



class TestGetInvoiceById(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app.app)

    def test_invoice_found(self):
        fake_invoice = {
            "InvoiceId": "INV-1",
            "VendorName": "ACME",
            "InvoiceDate": "2025-01-01",
            "BillingAddressRecipient": "John",
            "ShippingAddress": "Somewhere",
            "SubTotal": 100.0,
            "ShippingCost": 10.0,
            "InvoiceTotal": 110.0
        }

        # patch במקום שבו משתמשים בפונקציה (בתוך app.py)
        with patch("app.db_util.getInvoiceById", return_value=fake_invoice) as mock_get:
            response = self.client.get("/invoice/INV-1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["InvoiceId"], "INV-1")
        mock_get.assert_called_once_with("INV-1")

    def test_invoice_not_found(self):
        with patch("app.db_util.getInvoiceById", return_value=None):
            resp = self.client.get("/invoice/INV-404")

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json(), {"detail": "Invoice not found"})


if __name__ == "__main__":
    unittest.main() """

