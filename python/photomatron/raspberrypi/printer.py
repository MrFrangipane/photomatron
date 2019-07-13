import cups


class Printer:

    def print_picture(self, filepath, printer_name):
        print("Printer : '{}' prints {}".format(printer_name, filepath))

        conn = cups.Connection()
        conn.printFile(printer_name, filepath, 'Photomatron', {})
