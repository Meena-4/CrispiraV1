# Crispira V1 Prototype - Realistic gRNA scoring with basic off-target model

import streamlit as st
import random

# --- Sample Reference for Testing ---
sample_dna = "ATGCGTACCGTGGATCCGTACGTTAGCTAGCTGACTGGACCTGAGCCTGA"

# --- Simulated Azimuth Scoring (replace with real model/API later) ---
def azimuth_score(seq):
    gc = seq.count('G') + seq.count('C')
    gc_content = gc / len(seq)
    return round(0.4 + 0.5 * gc_content + random.uniform(-0.05, 0.05), 2)

# --- Off-target scoring: penalize seed mismatches and GC-rich sequences ---
def off_target_score(seq, genome=None):
    seed = seq[:12]  # Simplified seed region
    mismatches = seed.count('A')  # Simulate off-target by base imbalance
    penalty = mismatches * 0.01
    return round(0.05 + penalty + random.uniform(0, 0.02), 3)

# --- Ethics Flags ---
def ethics_flag(gene):
    flagged = ["FOXP2", "MYC", "CCR5", "BRCA1", "TP53"]
    if gene.upper() in flagged:
        return f"⚠️ Gene '{gene}' is ethically sensitive"
    return "✅ No major ethical issues flagged."

# --- Streamlit App Layout ---
st.title("🧬 Crispira - CRISPR gRNA Optimizer (V1)")
st.subheader("Smarter, safer gRNA design with AI-powered scoring")

# --- Input ---
gene = st.text_input("🧬 Target Gene (e.g., BRCA1)", value="BRCA1")
dna_seq = st.text_area("🧪 Target DNA Sequence (30-100 bp)", value=sample_dna, height=120)

if st.button("🚀 Predict Optimal gRNAs"):
    if not gene or len(dna_seq) < 20:
        st.error("Enter a valid gene name and sequence > 30bp.")
    else:
        st.success("Top gRNA candidates below:")

        # --- gRNA generation (20mers) ---
        candidates = [dna_seq[i:i+20] for i in range(0, len(dna_seq) - 19)]
        results = []

        for seq in candidates:
            on_score = azimuth_score(seq)
            off_score = off_target_score(seq)
            results.append((seq, on_score, off_score))

        results.sort(key=lambda x: (x[1] - x[2]), reverse=True)

        st.markdown("### 🎯 Ranked gRNAs")
        for i, (seq, on, off) in enumerate(results[:5]):
            st.code(f"gRNA #{i+1}: {seq}")
            st.write(f"- On-target score: {on}")
            st.write(f"- Off-target risk: {off}")
            st.markdown("---")

        st.markdown("### 🧠 Ethical Review")
        st.info(ethics_flag(gene))
