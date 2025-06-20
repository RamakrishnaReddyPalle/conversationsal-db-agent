#!/bin/bash
export $(grep -v '^#' .env | xargs)
mongosh "mongodb+srv://${MONGO_USER}:${MONGO_PASS}@sylvr-financial-cluster.jz9cn66.mongodb.net/admin"
