# -*- coding: utf-8 -*-

from django.test import TestCase

from catalogue.models import _d
from catalogue.work_importer import WorkImporter


class TestWorkImporter(TestCase):

    def setUp(self):
        work_path = 'catalogue/tests/docs/Opus 1'
        self.work_importer = WorkImporter(work_path)

    def test_import(self):
        self.work_importer.import_work()
        work = self.work_importer.get_work()

        self.assertEqual('Opus 1', work.code)
        self.assertEqual('RONDO OPUS 1', work.title)
        self.assertTrue(work.has_opus)
        self.assertFalse(work.is_posthumous)
        self.assertEqual(1, work.sort_order)
        self.assertEqual(18, len(self.work_importer.get_impressions()))

    def test__import_heading(self):
        heading = self.work_importer._import_heading(
            'catalogue/tests/docs/Opus 1/Op.1.heading.pdf')
        self.assertIsNotNone(heading)

    def test__import_order_of_impressiosn(self):
        expected = _d('1–1-BRZ')
        order_of_impressions = \
            self.work_importer._import_order_of_impressions()

        self.assertIsNotNone(order_of_impressions)
        self.assertEqual(expected, order_of_impressions[0])
