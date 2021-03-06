from typing import List
from pydantic import StrictStr
from spacy.language import Language
from .types import Example, TextSpanLabel


class EntityRecognizer:

    @property
    def labels(self) -> List[str]:
        """Return List of String Labels
        
        ### Raises
        -----------
        NotImplementedError: 
            Not Implemented, override
        
        ### Returns
        -----------
        (List[str]): 
            List of labels the model can predict
        """
        raise NotImplementedError

    def predict(self, texts: List[StrictStr]) -> List[Example]:
        """Run model inference on a batch of raw texts.
        
        ### Parameters
        --------------
        **texts**: (List[StrictStr]), required.
            Raw text examples
        
        ### Raises
        -----------
        NotImplementedError: 
            Not implemented, override
        
        ### Returns
        -----------
        (List[Example]): 
            List of Examples constructed from Model predictions
        """
        raise NotImplementedError


class SpacyEntityRecognizer(EntityRecognizer):

    def __init__(self, nlp: Language):
        super().__init__()
        self.nlp = nlp
    
    @property
    def labels(self) -> List[str]:
        """Return List of spaCy ner labels
        
        ### Returns
        -----------
        (List[str]): 
            List of labels from spaCy ner pipe
        """
        all_labels = set()

        for pipe in ['ner', 'entity_ruler']:
            if self.nlp.has_pipe(pipe):
                all_labels = all_labels | set(self.nlp.get_pipe(pipe).labels)

        return sorted(list(all_labels))


    def predict(self, texts: List[StrictStr]) -> List[Example]:
        """Run spaCy nlp.pipe on a batch of raw texts.
        
        ### Parameters
        --------------
        **texts**: (List[StrictStr]), required.
            Raw text examples
        
        ### Returns
        -----------
        (List[Example]): 
            List of Examples constructed from spaCy Model predictions
        """
        examples: List[Example] = []

        for doc in self.nlp.pipe(texts):
            examples.append(Example(
                text=doc.text,
                spans=[TextSpanLabel(text=e.text,
                                     start=e.start_char,
                                     end=e.end_char,
                                     label=e.label_)
                                     for e in doc.ents]
            ))
        return examples
