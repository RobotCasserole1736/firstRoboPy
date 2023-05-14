from ipykernel.kernelbase import Kernel

class TrainingKernel(Kernel):
    implementation = 'RobotPy Training'
    implementation_version = '1.0'
    language = 'py'
    language_version = '3.11'
    language_info = {
        'name': 'echo',
        'mimetype': 'text/py',
        'file_extension': '.py',
    }
    banner = "RobotPy Training Kernel Client"

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:
            stream_content = {'name': 'stdout', 'text': "[Peachy!]" + code}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }
