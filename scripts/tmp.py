from pygame.math import Vector2

def eval_expression(expr, context=None):
    context = context or {}
    try:
        return eval(expr, {"__builtins__": {}}, context)
    except Exception:
        return expr


ctx = {"Vector2": Vector2}
result = eval_expression("Vector2(3,5)", ctx)
print(result)
print(type(result))

print(eval("Vector2(4,8)", {}, ctx))