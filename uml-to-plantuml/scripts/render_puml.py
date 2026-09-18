#!/usr/bin/env python3
"""render_puml.py — 渲染并校验 PlantUML 图（零本地依赖）。

用法:
    python render_puml.py diagram.puml                 # 渲染为 PNG，输出到同目录
    python render_puml.py diagram.puml --format svg    # 渲染为 SVG
    python render_puml.py diagram.puml --out images/   # 指定输出目录
    python render_puml.py --check diagram.puml         # 仅校验语法（不产出图片）

渲染后端:
  1. Kroki (https://kroki.io) — POST 源码，无需 Java/Graphviz；失败时回读错误文本。
  2. plantuml.com 公共服务器 — 使用 deflate+hex 编码的 GET 兜底。

退出码: 0=成功且输出为真实图片; 2=语法/渲染错误(错误信息已打印); 3=网络或后端不可用。
"""
import argparse
import os
import sys
import urllib.request
import zlib

KROKI_URL = "https://kroki.io/plantuml/{fmt}"
PLANTUML_URL = "https://www.plantuml.com/plantuml/{fmt}/{enc}"

PNG_MAGIC = b"\x89PNG"
SVG_MAGIC = b"<svg"


def encode_plantuml(text: str) -> str:
    """PlantUML 官方 deflate+hex 编码（用于 plantuml.com GET 接口）。"""
    data = zlib.compress(text.encode("utf-8"))[2:-4]
    out = []

    def enc6(b: int) -> str:
        if b < 10:
            return chr(b + 48)
        if b < 36:
            return chr(b - 10 + 65)
        if b < 62:
            return chr(b - 36 + 97)
        return "-" if b == 62 else "_"

    for i in range(0, len(data), 3):
        b = data[i:i + 3]
        out.append(enc6(b[0] >> 2))
        out.append(enc6(((b[0] & 0x3) << 4) | ((b[1] >> 4) if len(b) > 1 else 0)))
        if len(b) > 1:
            out.append(enc6(((b[1] & 0xF) << 2) | ((b[2] >> 6) if len(b) > 2 else 0)))
        if len(b) > 2:
            out.append(enc6(b[2] & 0x3F))
    return "".join(out)


def looks_like_image(data: bytes, fmt: str) -> bool:
    if fmt == "svg":
        head = data.lstrip()[:200].lower()
        return b"<svg" in head or b"<?xml" in head
    return data[:4] == PNG_MAGIC


def render_kroki(source: str, fmt: str, timeout: int = 30):
    """返回 (ok, bytes_or_error_text)。"""
    url = KROKI_URL.format(fmt=fmt)
    req = urllib.request.Request(
        url, data=source.encode("utf-8"), headers={"Content-Type": "text/plain"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            if looks_like_image(data, fmt):
                return True, data
            return False, f"Kroki 返回了非图片内容（前 120 字节）: {data[:120]!r}"
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:2000]
        return False, f"Kroki HTTP {e.code}: {body}"  # 400 时 body 即 PlantUML 语法错误信息
    except Exception as e:
        return False, f"Kroki 请求失败: {e}"


def render_plantuml_com(source: str, fmt: str, timeout: int = 30):
    url = PLANTUML_URL.format(fmt=fmt, enc=encode_plantuml(source))
    req = urllib.request.Request(url, headers={"User-Agent": "render_puml/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            if looks_like_image(data, fmt):
                return True, data
            return False, f"plantuml.com 返回了非图片内容（前 120 字节）: {data[:120]!r}"
    except urllib.error.HTTPError as e:
        return False, f"plantuml.com HTTP {e.code}"
    except Exception as e:
        return False, f"plantuml.com 请求失败: {e}"


def main() -> int:
    ap = argparse.ArgumentParser(description="渲染并校验 PlantUML 图（Kroki / plantuml.com）")
    ap.add_argument("file", help=".puml 源文件路径")
    ap.add_argument("--format", choices=["png", "svg"], default="png")
    ap.add_argument("--out", help="输出目录（默认与源文件同目录）")
    ap.add_argument("--check", action="store_true", help="仅校验语法，不保存图片")
    args = ap.parse_args()

    if not os.path.isfile(args.file):
        print(f"错误: 文件不存在 {args.file}", file=sys.stderr)
        return 3
    source = open(args.file, encoding="utf-8").read()

    backends = [("Kroki", render_kroki), ("plantuml.com", render_plantuml_com)]
    errors = []
    for name, fn in backends:
        ok, payload = fn(source, args.format)
        if ok:
            if args.check:
                print(f"[OK] 语法校验通过（{name}）: {args.file}")
                return 0
            out_dir = args.out or os.path.dirname(os.path.abspath(args.file))
            os.makedirs(out_dir, exist_ok=True)
            base = os.path.splitext(os.path.basename(args.file))[0]
            out_path = os.path.join(out_dir, f"{base}.{args.format}")
            with open(out_path, "wb") as f:
                f.write(payload)
            print(f"[OK] {name} 渲染成功: {out_path} ({len(payload)} bytes)")
            return 0
        errors.append(f"[{name}] {payload}")

    print("渲染失败，后端错误如下：", file=sys.stderr)
    for e in errors:
        print(e, file=sys.stderr)
    # HTTP 400/500 = 服务器已解析图源并拒绝（语法/标签错误，见 workflow.md 排错表）；403/超时 = 网络问题
    return 2 if any(("HTTP 400" in e or "HTTP 500" in e) for e in errors) else 3


if __name__ == "__main__":
    sys.exit(main())
