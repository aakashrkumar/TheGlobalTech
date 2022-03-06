from wagtail_content_import.mappers.converters import ImageConverter, RichTextConverter, TableConverter, TextConverter
from wagtail_content_import.mappers.streamfield import StreamFieldMapper

from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.blocks import CharBlock, RichTextBlock, StreamBlock
from wagtail.contrib.table_block.blocks import TableBlock

class MyMapper(StreamFieldMapper):
    html = RichTextConverter('paragraph')
    image = ImageConverter('image')
    heading = TextConverter('heading')
    table = TableConverter('my_table_block')


class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """
    my_heading_block = CharBlock()
    my_paragraph_block = RichTextBlock()
    my_image_block = ImageChooserBlock()
    my_table_block = TableBlock()
