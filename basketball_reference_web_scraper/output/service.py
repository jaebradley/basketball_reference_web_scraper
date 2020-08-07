from basketball_reference_web_scraper.data import OutputType


class OutputService:
    def __init__(self, json_writer, csv_writer):
        self.json_writer = json_writer
        self.csv_writer = csv_writer
        self.output_type_writers = {
            OutputType.JSON: self.json_writer,
            OutputType.CSV: self.csv_writer,
        }

    def output(self, data, options):
        if options.output_type is None:
            return data

        writer = self.output_type_writers.get(options.output_type)

        if writer is None:
            raise ValueError("Unknown output type: {output_type}".format(output_type=options.output_type))

        return writer.write(data=data, options=options)




