import os
import networkx as nx
from androguard.misc import AnalyzeAPK

class AndroGuard:
    def __init__(self, path):
        self.path = path
        self.dir = os.path.dirname(path)
        self.a, self.d, self.dx = AnalyzeAPK(path)

    def get_opcodes(self):
        """
        Returns all opcodes which are not external. 

        params:

        return:
            ops: (list) opcodes array
        """
        ops = []
        for method in self.dx.get_methods():
            if method.is_external():
                continue
            # Need to get the EncodedMethod from the MethodClassAnalysis object
            m = method.get_method()
            if m.get_code():
                # get_code() returns None or a DalvikCode object
                # get_bc() returns a DCode object
                # get_raw() returns bytearray
                ops.append(m.get_code().get_bc().get_raw())
                
        return ops

    def get_method_counts(self):
        """
        Returns the method count from the `dx` analysis object
        
        params:

        return:
            ret: (dict) Count dictionary
        """
        from collections import defaultdict
        from operator import itemgetter
        ret = defaultdict(int)

        for method in self.dx.get_methods():
            if method.is_external():
                continue
            m = method.get_method()
            for ins in m.get_instructions():
                ret[(ins.get_op_value(), ins.get_name())] += 1

        for k, v in sorted(ret.items(), key=itemgetter(1), reverse=True)[:10]:
            print(k, '-->',  v)
        
        return ret

    def get_ast(self):
        """
        Returns the abstract syntax tree.

        params:

        return:
            ret : dict (per method lists the ast)
        """
        from androguard.decompiler.dad.decompile import DvMethod
        ret = {}
        for method in self.dx.get_methods():
            if method.is_external():
                continue
            dv = DvMethod(self.dx.get_method(method.get_method()))
            dv.process(doAST=True)
            ret[method] = dv.get_ast()
        return ret

    def get_metadata(self):
        """
        Returns the metadata (i.e., package name, app name, so on)

        params:

        return:
            metadata : JSON object
        """
        pass

    def get_cg(self):
        """
        Returns the call graph of from the `dx` analysis object
        """
        return self.dx.get_call_graph()

    def save_cg(self, fmt="gml"):
        nxg = self.dx.get_call_graph()
        
        if fmt == "gml":
            nx.write_gml(nxg, os.path.join(self.dir, "cg.gml"))

        return self

    def get_method_for_class(self, className):
        """
        Returns the method calls from the cross references.

        params:
            className: (str) Class name to be queried.

        return:
            methods: (list) List of methods belonging to a class.
        """
        methods = []
        try:
            class_obj = self.dx.classes[className]
            for meth in class_obj.get_methods():
                print("usage of method {}".format(meth.name))
                for _, call, _ in meth.get_xref_from():
                    print("  called by -> {} -- {}".format(call.class_name, call.name))
                    methods.append(call.name)
        except Exception:
            pass

        return methods
    
    def get_method_for_all_classes(self):
        """
        Returns the method calls from the cross references.

        """
        all_classes = {}
        for cls in self.dx.get_classes():
            className = cls.orig_class.get_name()
            print(f"---------------------{className}----------------------")
            all_classes[className] = self.get_method_for_class(self.dx, className)
        return all_classes