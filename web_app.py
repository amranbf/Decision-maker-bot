import streamlit as st
from decision_bot import DecisionBot
import json

st.set_page_config(page_title="Decision Maker Bot", page_icon="🤖", layout="wide")

if 'bot' not in st.session_state:
    st.session_state.bot = DecisionBot()
    st.session_state.current_factors = []
    st.session_state.current_options = []

st.title("🤖 Decision Maker Bot")
st.markdown("### AI-Powered Decision Analysis Tool")

tab1, tab2, tab3 = st.tabs(["📝 New Decision", "📊 Analysis", "📜 History"])

with tab1:
    st.header("Create a New Decision")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        question = st.text_input("What decision are you trying to make?", 
                                placeholder="e.g., Which job offer should I accept?")
    
    with col2:
        options_input = st.text_input("Options (comma-separated)", 
                                     placeholder="e.g., Job A, Job B, Job C")
    
    if st.button("Create Decision", type="primary"):
        if question and options_input:
            options = [opt.strip() for opt in options_input.split(',')]
            if len(options) >= 2:
                st.session_state.bot.create_decision(question, options)
                st.session_state.current_options = options
                st.session_state.current_factors = []
                st.success(f"✅ Decision created with {len(options)} options!")
            else:
                st.error("Please enter at least 2 options")
        else:
            st.error("Please fill in both question and options")
    
    st.divider()
    
    st.subheader("Add Decision Factors")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        factor_name = st.text_input("Factor name", placeholder="e.g., Salary, Location")
    
    with col2:
        importance = st.number_input("Importance (1-10)", min_value=1, max_value=10, value=5)
    
    with col3:
        st.write("")
        st.write("")
        if st.button("Add Factor"):
            if factor_name and st.session_state.bot.current_decision:
                st.session_state.bot.add_factor(factor_name, importance)
                st.session_state.current_factors.append(factor_name)
                st.success(f"✅ Added: {factor_name}")
            elif not st.session_state.bot.current_decision:
                st.error("Create a decision first!")
            else:
                st.error("Enter a factor name")
    
    if st.session_state.current_factors:
        st.write("**Current Factors:**")
        for i, factor in enumerate(st.session_state.current_factors, 1):
            st.write(f"{i}. {factor}")
    
    st.divider()
    
    st.subheader("Rate Your Options")
    
    if st.session_state.current_options and st.session_state.current_factors:
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
        
        with col1:
            selected_option = st.selectbox("Select Option", st.session_state.current_options)
        
        with col2:
            selected_factor = st.selectbox("Select Factor", st.session_state.current_factors)
        
        with col3:
            rating = st.number_input("Rating (1-10)", min_value=1, max_value=10, value=5, key="rating")
        
        with col4:
            st.write("")
            st.write("")
            if st.button("Add Rating"):
                st.session_state.bot.add_rating(selected_option, selected_factor, rating)
                st.success(f"✅ Rated {selected_option} - {selected_factor}: {rating}")
    else:
        st.info("Create a decision and add factors first to start rating options")

with tab2:
    st.header("Decision Analysis")
    
    if st.button("🔍 Analyze Decision", type="primary"):
        if st.session_state.bot.current_decision:
            if st.session_state.bot.current_decision.factors:
                analysis = st.session_state.bot.analyze()
                
                if analysis:
                    st.success("✅ Analysis Complete!")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Recommended Option", analysis['recommended'])
                        st.metric("Confidence Level", f"{analysis['confidence']}%")
                    
                    with col2:
                        if analysis['is_close_call']:
                            st.warning("⚠️ CLOSE CALL: Top options are very similar!")
                        st.write("**Key Factors:**")
                        st.write(", ".join(analysis['key_factors']))
                    
                    st.divider()
                    
                    st.subheader("Detailed Scores")
                    
                    for option, score in analysis['scores'].items():
                        st.write(f"**{option}:** {score} points")
                        st.progress(score / max(analysis['scores'].values()) if max(analysis['scores'].values()) > 0 else 0)
                    
                    if analysis['warnings']:
                        st.divider()
                        st.subheader("⚠️ Warnings")
                        for warning in analysis['warnings']:
                            st.warning(warning)
            else:
                st.error("Please add at least one factor before analyzing")
        else:
            st.error("Please create a decision first")
    
    st.divider()
    
    if st.session_state.bot.current_decision:
        st.subheader("Current Decision Summary")
        st.write(f"**Question:** {st.session_state.bot.current_decision.question}")
        st.write(f"**Options:** {', '.join(st.session_state.bot.current_decision.options)}")
        
        if st.session_state.bot.current_decision.factors:
            st.write("**Factors:**")
            for factor, importance in st.session_state.bot.current_decision.factors.items():
                st.write(f"- {factor} (Importance: {importance})")

with tab3:
    st.header("Decision History")
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    with col2:
        if st.button("📊 View Statistics"):
            stats = st.session_state.bot.get_statistics()
            if isinstance(stats, dict):
                st.metric("Total Decisions", stats['total_decisions'])
                st.metric("Average Confidence", f"{stats['average_confidence']}%")
            else:
                st.info(stats)
    
    st.divider()
    
    history = st.session_state.bot.get_history()
    
    if history:
        for i, decision in enumerate(reversed(history), 1):
            with st.expander(f"Decision {len(history) - i + 1}: {decision['question']}"):
                st.write(f"**Options:** {', '.join(decision['options'])}")
                st.write(f"**Recommended:** {decision['chosen']}")
                st.write(f"**Confidence:** {decision['confidence']}%")
    else:
        st.info("No decision history yet. Make your first decision!")