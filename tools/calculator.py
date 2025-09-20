# Safe calculator using ast parse
import ast, operator as op, math

# supported operators
operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg
}

def eval_expr(expr):
    """Evaluate arithmetic expression safely."""
    node = ast.parse(expr, mode='eval').body
    return _eval(node)

def _eval(node):
    if isinstance(node, ast.Num):
        return node.n
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        oper = operators[type(node.op)]
        return oper(left, right)
    if isinstance(node, ast.UnaryOp):
        oper = operators[type(node.op)]
        return oper(_eval(node.operand))
    raise TypeError(node)

class Calculator:
    def run(self, args):
        expr = args.get('expression','')
        # handle percent e.g., '12% of 1340 + 50' -> convert '12% of 1340' to '(0.12*1340)'
        expr = expr.replace('%','/100')
        expr = expr.replace(' of ', '*')
        try:
            val = eval_expr(expr)
            return {'expression': expr, 'value': val}
        except Exception as e:
            raise e
