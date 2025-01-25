from typing import Protocol as ProtocolistProtocol
from typing import runtime_checkable







@runtime_checkable
class File(ProtocolistProtocol):
	
	def read(self, arg0: int):
		...
	def seek(self, arg0):
		...
	def tell(self):
		...
