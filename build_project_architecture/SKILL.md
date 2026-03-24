---
name: build_project_architecture
description: >-
  This skill should be used when users want to analyze a software project's source code
  and generate a comprehensive architecture design document in PDF format (primarily in Chinese).
  It covers core architecture diagrams, flowcharts, sequence diagrams, design pattern analysis,
  and key scenario call chains. Trigger phrases include "生成架构文档", "分析项目架构",
  "生成设计文档", "architecture document", "design document", "模块设计", "源码分析",
  or when the user asks to read source code and produce an architecture/design PDF.
---

# Build Project Architecture Skill

## Purpose

Analyze a software project module's source code and generate a comprehensive architecture design document in PDF format, primarily written in Chinese. The document covers:

1. **核心架构设计** — Architecture diagrams, module layering, class hierarchy
2. **流程图与时序图** — Core workflow charts and sequence diagrams
3. **设计模式分析** — Design pattern identification and explanation for key classes
4. **关键场景调用链** — Call chain analysis for important usage scenarios

## When To Use

- User requests analysis of a project/module's source code architecture
- User asks to generate a design document (设计文档) or architecture document (架构文档)
- User wants flowcharts, sequence diagrams, or design pattern analysis of source code
- User mentions "源码分析", "模块设计", "架构设计", "生成PDF"

## Workflow

### Phase 1: Source Code Exploration

1. **Identify the target module/directory** from user's request. If not explicitly specified, ask the user to clarify which module or directory to analyze.

2. **Explore the module structure** using the code-explorer subagent:
   - List all source files recursively
   - Identify the primary programming language (Java, Scala, Python, etc.)
   - Count total files to estimate scope

3. **Read ALL source files** in the target module. For modules with many files, prioritize:
   - Core/entry-point classes (Main, Application, Catalog, Manager, etc.)
   - Interface definitions and abstract base classes
   - Implementation classes
   - Configuration/properties classes
   - Utility classes

4. **Identify inheritance hierarchies** — Find parent classes/interfaces that may live outside the target module. Read those as well to understand the full design.

### Phase 2: Architecture Analysis

Perform the following analyses on the source code:

#### 2.1 Architecture Design (架构设计)

- Identify the **layered architecture** (API layer, Core layer, Implementation layer, etc.)
- Map **class relationships** (inheritance, composition, dependency)
- Identify **external dependencies** and integration points
- Create a **module file inventory** with brief descriptions of each class's role
- If applicable, create a **concept mapping table** (e.g., how project concepts map to external system concepts)

#### 2.2 Flowcharts (流程图)

- Identify **2-4 core workflows** in the module (e.g., initialization flow, data processing flow, commit flow)
- For each workflow, trace the execution path through the code
- Document decision points, loops, and error handling branches
- Represent flows using ASCII-art style box diagrams suitable for PDF rendering

#### 2.3 Sequence Diagrams (时序图)

- Identify **2-3 key multi-component interactions** (e.g., client→catalog→table→storage)
- Trace the method call sequence across class boundaries
- Document request/response patterns and data transformations
- Represent using participant-based sequence notation

#### 2.4 Design Patterns (设计模式)

For each core class, identify applicable design patterns:

- **Creational**: Factory Method, Abstract Factory, Builder, Singleton
- **Structural**: Adapter, Bridge, Composite, Decorator, Facade, Proxy
- **Behavioral**: Strategy, Template Method, Observer, Iterator, Chain of Responsibility, Command, State, Visitor
- **Concurrency**: Optimistic Locking, Retry, Immutable Object

For each pattern found, explain:
- Which class implements it
- How it is implemented (key methods/interfaces)
- Why this pattern was chosen (design intent)

#### 2.5 Key Scenario Call Chains (关键场景调用链)

Identify **4-6 important usage scenarios** and trace the complete call chain:

- Entry point → intermediate calls → final execution
- Include method signatures and brief descriptions
- Highlight important state transitions and side effects

### Phase 3: PDF Document Generation

#### 3.1 Document Structure

Generate a PDF with the following chapters:

1. **模块概述** — Module overview, positioning, and responsibilities
2. **核心架构设计** — Architecture diagram, file inventory, class hierarchy
3. **设计模式详解** — Pattern analysis for each core class
4. **核心流程图** — 2-4 workflow diagrams with step descriptions
5. **时序图** — 2-3 sequence diagrams showing component interactions
6. **关键场景调用链** — 4-6 scenario call chains with detailed steps
7. **配置与扩展** — Configuration properties, extension points (if applicable)
8. **设计亮点与总结** — Design highlights, limitations, quality assessment

#### 3.2 PDF Generation

Use the bundled Python script at `scripts/generate_pdf.py` to generate the PDF.

**IMPORTANT**: The script is a **template/framework** — it provides the PDF generation infrastructure (fonts, styles, page layout, Chinese text support, diagram drawing utilities). The actual document content must be filled in by Claude based on the source code analysis.

**Execution steps:**

1. Read the script from `scripts/generate_pdf.py`
2. Create a **project-specific** copy of the script in the project's root directory (e.g., `generate_doc.py`)
3. **Modify the content sections** of the copied script to include:
   - Analysis results from Phase 2
   - Module-specific architecture diagrams
   - Actual class names, method signatures, and descriptions
   - Real flowchart and sequence diagram data
4. Execute the script: `python3 generate_doc.py`
5. Verify the PDF was generated successfully
6. Clean up: delete the temporary script file

**Font handling for macOS:**
- Primary: `/System/Library/Fonts/STHeiti Light.ttc` (subfontIndex=0)
- Fallback: `/System/Library/Fonts/Hiragino Sans GB.ttc` (subfontIndex=0)
- Fallback: `/System/Library/Fonts/PingFang.ttc` (subfontIndex=0)

**Font handling for Linux:**
- Primary: `/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc` (subfontIndex=0)
- Fallback: `/usr/share/fonts/truetype/wqy/wqy-microhei.ttc` (subfontIndex=0)

#### 3.3 PDF Naming Convention

Name the PDF file as: `{Project}_{Module}_Design_Document.pdf`

Examples:
- `Iceberg_BigQuery_Module_Design_Document.pdf`
- `Iceberg_Core_Design_Document.pdf`
- `Spring_WebMVC_Design_Document.pdf`

Place the PDF in the **project root directory**.

### Phase 4: Git Commit and Push

After PDF generation:

1. `git add <pdf-filename>`
2. Commit with message format:
   ```
   docs(<module>): add/update <module> architecture design document

   Generated comprehensive architecture design document with:
   - Core architecture diagram with layered design
   - N workflow flowcharts
   - N sequence diagrams
   - Design pattern analysis for N core classes
   - N key scenario call chains

   --story=0
   ```
3. Push to the current branch

## Quality Standards

### Document Quality

- All text in Chinese (中文) except for code identifiers and technical terms
- Architecture diagrams must reflect actual code structure, not generic patterns
- Every class mentioned must exist in the source code
- Call chains must trace real method calls, not hypothetical ones
- Design patterns must be genuinely present in the code, not forced

### Diagram Quality

- Flowcharts use consistent box/arrow notation
- Sequence diagrams clearly show participants and message flow
- All diagrams have descriptive titles and legends where needed
- ASCII-art diagrams should be readable and well-aligned

### Completeness Checklist

- [ ] All source files in the target module have been read
- [ ] Parent classes/interfaces outside the module have been examined
- [ ] At least 2 flowcharts are included
- [ ] At least 2 sequence diagrams are included
- [ ] At least 3 design patterns are identified and explained
- [ ] At least 4 key scenario call chains are documented
- [ ] PDF is generated and placed in project root
- [ ] PDF is committed and pushed to remote

## Troubleshooting

### Common Issues

1. **reportlab not installed**: Run `pip3 install reportlab`
2. **Font not found**: Check OS-specific font paths listed above; try alternative fonts
3. **TTC font loading timeout**: Use `subfontIndex=0` parameter when registering TTC fonts
4. **Script timeout**: If the Python script takes too long, check for large font file loading; use STHeiti Light as primary font on macOS
5. **PDF too large**: Limit embedded diagrams; use text-based representations instead of images

### Dependency

- Python 3.6+
- reportlab library (`pip3 install reportlab`)
