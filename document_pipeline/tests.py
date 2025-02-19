from PyPDF2 import PdfReader
from datetime import datetime
from pipeline import ShareStorageService, ContentExtractionService, PDF

class BaseTestingClass:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0 

    def run_test(self, test_func):
        self.tests_run += 1
        test_name = test_func.__name__
        try:
            print(f"\nRunning test: {test_name}...")
            test_func()
            self.tests_passed += 1
            print(f"✓ {test_name} passed")
        except AssertionError as e:
            print(f"✗ {test_name} failed: {str(e)}")
        except Exception as e:
            print(f"✗ {test_name} failed with error: {str(e)}")

    def run(self):
        test_methods = [method for method in dir(self) 
                       if method.startswith('test_')]
        for test_method in test_methods:
            self.run_test(getattr(self, test_method))
        
        print(f"\nTests run: {self.tests_run}")
        print(f"Tests passed: {self.tests_passed}")
        print(f"Tests failed: {self.tests_run - self.tests_passed}")

        return self.tests_passed == self.tests_run

class ShareStorageServiceTests(BaseTestingClass):
    def __init__(self):
        super().__init__()
        self.storage = ShareStorageService('./')

    def test_read_pdf(self):
        pdf = self.storage.read_pdf('input.pdf')
        assert pdf is not None

class ContentExtractionServiceTests(BaseTestingClass):
    def __init__(self):
        super().__init__()
        self.content_extractor = ContentExtractionService()
        self.pdf = PDF(
            fund_name='Test',
            upload_timestamp=datetime.today(),
            filename='test.pdf',
            contents=PdfReader('./input.pdf')
        )

    def test_extract(self):
        self.content_extractor.extract(self.pdf)

if __name__ == "__main__":
    storage_tests = ShareStorageServiceTests()
    extractor_tests = ContentExtractionServiceTests()

    extractor_tests.run()
    storage_tests.run()