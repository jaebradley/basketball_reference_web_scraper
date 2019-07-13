from basketball_reference_web_scraper.data import OutputType, OutputWriteOption
from basketball_reference_web_scraper.json_encoders import JSONEncoder
from basketball_reference_web_scraper.writers import JSONWriter, WriteOptions


def output(values, output_type, output_file_path, csv_writer, output_write_option=None, json_options=None):
    if output_type is None:
        return values

    write_option = OutputWriteOption.WRITE if output_write_option is None else output_write_option

    if output_type == OutputType.JSON:
        options = WriteOptions(file_path=output_file_path, mode=write_option, custom_options=json_options)
        writer = JSONWriter(encoder=JSONEncoder())
        return writer.write(data=values, options=options)

    if output_type == OutputType.CSV:
        options = WriteOptions(file_path=output_file_path, mode=write_option)
        csv_writer.write(data=values, options=options)

    raise ValueError("Unknown output type: {output_type}".format(output_type=output_type))
