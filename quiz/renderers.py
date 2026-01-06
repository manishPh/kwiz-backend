# -*- coding: utf-8 -*-
"""
Custom JSON renderer to ensure proper UTF-8 encoding of emojis and Unicode characters.
"""
from rest_framework.renderers import JSONRenderer
import json


class UTF8JSONRenderer(JSONRenderer):
    """
    Custom JSON renderer that ensures UTF-8 encoding and doesn't escape Unicode characters.
    This fixes the issue where emojis (🎬, 🏆, etc.) were being displayed as � characters.
    """
    charset = 'utf-8'
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, ensuring UTF-8 encoding and no Unicode escaping.
        """
        if data is None:
            return b''
        
        # Use ensure_ascii=False to preserve Unicode characters (emojis)
        ret = json.dumps(
            data,
            cls=self.encoder_class,
            ensure_ascii=False,
            allow_nan=not self.strict,
            **self.get_indent(accepted_media_type, renderer_context)
        )
        
        # Encode to UTF-8 bytes
        return ret.encode('utf-8')

