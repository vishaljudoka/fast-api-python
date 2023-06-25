import time
import unittest
import pytest
from main import app
from fastapi.testclient import TestClient
from fastapi import status

client=TestClient(app=app)

raw_data= {
    "name": "TestMilk",
    "price": 4.5,
    "brand": "Pil"
    }
raw_data1= {
    "name": "TestMilk1",
    "price": 4.5,
    "brand": "Pil"
    }

def test_index_return_correct():
    response=client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'family' : 'vksh'}
""" 
#This will create actual entry in database , You can create seprate testing enc db and then test.
def test_post_return_correct():
    response=client.post('/create-item/' ,json = raw_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == "Item creted successfully"


def test_delete_return_correct():
    time.sleep(2)
    response=client.delete('/delete/' ,params= {'name':'TestMilk'})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.json() == status.HTTP_204_NO_CONTENT
"""

def test_post_return_bad_data():
    time.sleep(2)
    response=client.post('/create-item/' ,json = raw_data1)
    assert response.status_code == 400
    assert response.json() == {"detail" :"Item ID already exist"}



#pytest --verbose --junit-xml Test/results.xml test_main.py
