import streamlit as st
import uuid
import os
from dotenv import load_dotenv
from graph.builder import build_graph
from langchain_core.messages import HumanMessage
from fpdf import FPDF

load_dotenv()

# --- INITIALIZATION ---
if "history" not in st.session_state:
    st.session_state.history = []

if "app" not in st.session_state:
    st.session_state.app = build_graph()
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.config = {"configurable": {"thread_id": st.session_state.thread_id}}
    st.session_state.current_plan = None
    st.session_state.final_report = None
    st.session_state.waiting_for_approval = False
    st.session_state.current_topic = "" # Track topic for history naming

# --- SIDEBAR (Always Visible) ---
with st.sidebar:
    st.title("Settings & Status")
    st.markdown("---")
    st.subheader("Current Session")
    st.code(st.session_state.thread_id, language=None)
    
    if st.button("🔄 Start New Research"):
        # SURGICAL CLEAR: Keep history and app, clear the rest
        keys_to_keep = {"history", "app"}
        for key in list(st.session_state.keys()):
            if key not in keys_to_keep:
                del st.session_state[key]
        
        # Reset specific variables for the new run
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.config = {"configurable": {"thread_id": st.session_state.thread_id}}
        st.session_state.current_plan = None
        st.session_state.final_report = None
        st.session_state.waiting_for_approval = False
        st.session_state.current_topic = ""
        
        st.rerun()

    st.markdown("---")
    st.header("📜 Research History")
    
    if not st.session_state.history:
        st.info("No past reports yet.")
    else:
        # Show history in reverse order (newest first)
        for i, entry in enumerate(reversed(st.session_state.history)):
            with st.expander(f"{entry['topic'][:30]}..."):
                st.caption(f"Thread: {entry['id'][:8]}")
                if st.button("Load Report", key=f"load_{i}"):
                    st.session_state.final_report = entry['content']
                    st.session_state.current_topic = entry['topic']
                    st.session_state.waiting_for_approval = False
                    st.rerun()

# --- MAIN UI ---
st.title("🔍 Agentic Research Assistant")

# --- PHASE 1: INPUT ---
if not st.session_state.waiting_for_approval and not st.session_state.final_report:
    topic = st.text_input("What is your research topic?")
    if st.button("Generate Plan"):
        if topic:
            st.session_state.current_topic = topic # Save topic name
            with st.spinner("Planning..."):
                initial_input = {"messages": [HumanMessage(content=topic)]}
                for event in st.session_state.app.stream(initial_input, st.session_state.config, stream_mode="values"):
                    if "plan" in event:
                        raw_plan = event["plan"]
                        if isinstance(raw_plan, list) and len(raw_plan) > 0:
                            st.session_state.current_plan = raw_plan[0].get('text', str(raw_plan))
                        elif isinstance(raw_plan, dict):
                            st.session_state.current_plan = raw_plan.get('text', str(raw_plan))
                        else:
                            st.session_state.current_plan = str(raw_plan)
                
                st.session_state.waiting_for_approval = True
                st.rerun()

# --- PHASE 2: APPROVAL ---
if st.session_state.waiting_for_approval:
    st.subheader(f"Proposed Plan for: {st.session_state.current_topic}")
    st.info(st.session_state.current_plan)
    if st.button("✅ Approve & Research"):
        with st.spinner("Researching and Self-Reviewing..."):
            for event in st.session_state.app.stream(None, st.session_state.config, stream_mode="values"):
                last_msg = event["messages"][-1]
                st.session_state.final_report = last_msg.content
            
            # SAVE TO HISTORY AFTER COMPLETION
            st.session_state.history.append({
                "topic": st.session_state.current_topic,
                "content": st.session_state.final_report,
                "id": st.session_state.thread_id
            })
            
            st.session_state.waiting_for_approval = False
            st.rerun()

# --- PDF HELPER ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(5)
            continue
        if line.startswith('# '):
            pdf.set_font("Arial", 'B', 16)
            pdf.multi_cell(0, 10, line.replace('# ', '').encode('latin-1', 'ignore').decode('latin-1'))
            pdf.ln(5)
        elif line.startswith('## '):
            pdf.set_font("Arial", 'B', 13)
            pdf.multi_cell(0, 10, line.replace('## ', '').encode('latin-1', 'ignore').decode('latin-1'))
            pdf.ln(2)
        elif line == '---':
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)
        else:
            pdf.set_font("Arial", size=11)
            clean_line = line.replace('**', '').replace('*', '').replace('###', '')
            pdf.multi_cell(0, 7, clean_line.encode('latin-1', 'ignore').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')

# --- PHASE 3: OUTPUT ---
if st.session_state.final_report:
    st.subheader(f"📝 Final Research Report: {st.session_state.current_topic}")
    
    raw_content = st.session_state.final_report
    clean_report = ""
    if isinstance(raw_content, list) and len(raw_content) > 0:
        item = raw_content[0]
        clean_report = item.get('text', str(item)) if isinstance(item, dict) else str(item)
    elif isinstance(raw_content, dict):
        clean_report = raw_content.get('text', str(raw_content))
    else:
        clean_report = str(raw_content)

    st.markdown(clean_report)
    st.write("---")
    
    try:
        pdf_data = create_pdf(clean_report)
        st.download_button(
            label="📥 Download Report as PDF",
            data=pdf_data,
            file_name=f"{st.session_state.current_topic.replace(' ', '_')}_report.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"PDF Error: {e}")
        st.download_button("Download as .md (Backup)", data=clean_report, file_name="report.md")