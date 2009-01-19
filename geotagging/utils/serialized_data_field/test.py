# -*- coding: utf-8 -*-
"""Unit testing for this module."""

from django.test import TestCase
from django.db import models
from fields import PickledObjectField

class TestingModel(models.Model):
	pickle_field = PickledObjectField()

class TestCustomDataType(str):
	pass

class PickledObjectFieldTests(TestCase):
	def setUp(self):
		self.testing_data = (
			{1:1, 2:4, 3:6, 4:8, 5:10},
			'Hello World',
			(1, 2, 3, 4, 5),
			[1, 2, 3, 4, 5],
			TestCustomDataType('Hello World'),
		)
		return super(PickledObjectFieldTests, self).setUp()
	
	def testDataIntegriry(self):
		"""Tests that data remains the same when saved to and fetched from the database."""
		for value in self.testing_data:
			model_test = TestingModel(pickle_field=value)
			model_test.save()
			model_test = TestingModel.objects.get(id__exact=model_test.id)
			self.assertEquals(value, model_test.pickle_field)
			model_test.delete()
	
	def testLookups(self):
		"""Tests that lookups can be performed on data once stored in the database."""
		for value in self.testing_data:
			model_test = TestingModel(pickle_field=value)
			model_test.save()
			self.assertEquals(value, TestingModel.objects.get(pickle_field__exact=value).pickle_field)
			model_test.delete()