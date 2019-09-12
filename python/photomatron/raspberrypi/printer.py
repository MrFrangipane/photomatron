import json
import cups


class Printer:
    conn = cups.Connection()

    def print_picture(self, filepath, printer_name):
        print("Printer : '{}' prints {}".format(printer_name, filepath))

        job_id = Printer.conn.printFile(printer_name, filepath, 'Photomatron', {})

        with open(filepath + '.json', 'w+') as f_job:
            json.dump(Printer.conn.getJobAttributes(job_id), f_job, indent=2)
