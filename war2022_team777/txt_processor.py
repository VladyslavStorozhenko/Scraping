import os
import codecs


if __name__ == '__main__':
    for filename in os.listdir(os.path.dirname(os.path.realpath(__file__)) + '/sas_ready_txt'):
        with codecs.open('sas_ready_txt/' + filename, 'r+', 'utf-8-sig') as file:
            new_lines = []
            for n, line in enumerate(file):
                if n < 2:
                    new_lines.append(line)
                    continue
                if not line.isspace() and line[-2] == '.':
                    new_lines.append(line)
                elif not line.isspace() and line[-2] != '.':
                    new_lines.append(line[:-1])
            file.seek(0)
            file.writelines(new_lines)
