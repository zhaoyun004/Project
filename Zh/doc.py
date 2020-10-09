''' 生成用户手册 '''

import pdfkit
pdfkit.from_file(['Manual'], 'Manual.pdf')
