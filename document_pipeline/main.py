from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any
from PyPDF2 import PdfReader
from io import BytesIO

@dataclass
class PDF:
    """ Dataclass to manage the metadata for a PDF """
    fund_name: str
    upload_timestamp: datetime
    filename: str
    contents: bytes

@dataclass
class ExtractedMetrics:
    """ Container for extracted fund metrics """
    fund_size: float
    returns: float
    strategy_type: str
    management_fee: float
    performance_fee: float
    min_investment: float
    inception_data: datetime
    confidence_scores: Dict[str, float]

class ContentExtractionService:
    """ Service to handle the extraction of the content from the PDF """
    def extract(self, pdf: PDF) -> Dict[str, Any]:
        need_ocr = self._needs_ocr(pdf)
        if need_ocr:
            return self._extract_ocr(pdf)
        else:
            return self._extract_direct(pdf)

    def _needs_ocr(self, pdf: PDF) -> bool:
        return False

    def _extract_direct(self, pdf: PDF) -> Dict[str, Any]:
        pdf_file = BytesIO(pdf.contents)
        
        reader = PdfReader(pdf_file)
        
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
            
        return {
            "text": text
        }

    def _extract_ocr(self, pdf: PDF) -> Dict[str, Any]:
        pass

    def score(self):
        pass

class MetricExtractionService:
    """ Service to handle the extraction of the metrics from the PDF """
    def extract_metrics(self, pdf_content: str):
        return ExtractedMetrics(
            fund_size=12.0,
            returns=12.0,
            strategy_type='Macro',
            management_fee=5.0,
            performance_fee=5.0,
            min_investment=12000,
            inception_data=datetime.today(),
            confidence_scores={'main': 5.0}
        )

class MetricValidationService:
    """ Service to handle the validation of metrics extracted from the PDF """
    def validate_metrics(self, metrics: ExtractedMetrics):
        return True, 'yes'

class ShareStorageService:
    """ Class to interact with the pdf datalake of fund files """
    def __init__(self, location):
        self.location = location

    def read_pdf(self, file_name):
        path = self.location + file_name
        with open(path, 'rb') as file:
            pdf_content = file.read()

        return PDF(
            fund_name='Test Fund',
            upload_timestamp=datetime.today(),
            filename=file_name,
            contents=pdf_content
        )

    def write_pdf(self, file_name):
        pass

class PipelineError(Exception):
    """ Base exception for all pipeline-related errors """
    pass

class LowConfidenceError(PipelineError):
    """ Raised when confidenc score is below threshold """
    pass

class ValidationError(PipelineError):
    """ Raise when metrics fail validation """
    pass

class PdfProcessingPipeline:
    def __init__(self, 
                 content_extractor: ContentExtractionService,
                 metric_extractor: MetricExtractionService,
                 validator: MetricValidationService
                 ):
        self.content_extractor = content_extractor
        self.metric_extractor = metric_extractor
        self.validator = validator

    def process_pdf(self, pdf: PDF):
        content = self.content_extractor.extract(pdf)
        """ confidence = self.content_extractor.score()

        if confidence < 0.5:
            raise LowConfidenceError(f"Content extraction confidence: {confidence}") """
        
        metrics = self.metric_extractor.extract_metrics(content['text'])
        is_valid, messages = self.validator.validate_metrics(metrics)
        
        if not is_valid:
            raise ValidationError(messages)
        
        return metrics
    

if __name__ == "__main__":
    storage = ShareStorageService('./')
    pdf = storage.read_pdf('input.pdf')

    content_extractor = ContentExtractionService()
    metric_extractor = MetricExtractionService()
    validator = MetricValidationService()

    pipeline = PdfProcessingPipeline(content_extractor, metric_extractor, validator)
    metrics = pipeline.process_pdf(pdf)
    print(metrics)