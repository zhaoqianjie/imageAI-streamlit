#!/usr/bin/env python
# -*- coding: utf-8 -*-
import streamlit as st

USERNAME = st.secrets['username']
CATEGORY = "object_detection"
CATEGORY_KEY = "/".join([USERNAME, "object_detection"])
