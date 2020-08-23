# import tempfile
# import os
# def tempfile_tree():
#     file_names = []
#
#     for _ in range(5):
#         f_handle = tempfile.NamedTemporaryFile(delete=False)
#         os.rename(f_handle.name, f'{f_handle.name}.json')
#         file_names.append(f'{f_handle.name}.json')
#     return file_names
#
# tempfile_tree()


class A:
    def __init__(self, string):
        print(string)
        pass

    def create_a(self, string):
        a = A(string)
        #return a.create_a('c')


a = A('a')
a.create_a('b')
