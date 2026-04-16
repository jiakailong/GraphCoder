import ast

def chunk_python_code(code: str, max_lines_per_chunk: int = 150) -> list[str]:
    """
    Very crude AST-based chunker for Python files to avoid passing massive raw files into RAG.
    Parses top-level classes/functions and splits them logically instead of arbitrary line breaks.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        # Fallback to naive sliding window if not valid python
        lines = code.split('\n')
        return ['\n'.join(lines[i:i + max_lines_per_chunk]) for i in range(0, len(lines), max_lines_per_chunk)]

    chunks = []
    current_chunk = []
    current_lines = 0
    lines = code.split('\n')

    for node in tree.body:
        start = node.lineno - 1
        end = getattr(node, 'end_lineno', start + 1)
        node_code = '\n'.join(lines[start:end])
        
        node_lines = end - start

        if current_lines + node_lines > max_lines_per_chunk and current_chunk:
            chunks.append("\n".join(current_chunk))
            current_chunk = []
            current_lines = 0

        current_chunk.append(node_code)
        current_lines += node_lines

    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks
