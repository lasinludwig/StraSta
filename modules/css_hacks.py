"""CSS-edits to make the streamlit app look better"""
import streamlit as st

# Aussehen der labels (Überschriften)    {font-size:105%; font-weight:bold; font-style:italic; color:blue;}
CSS_LABEL_1 = "{font-size:1rem; font-weight:600}"
CSS_LABEL_2 = "{font-size:0.95rem; font-weight:600;}"


# Spaltenüberschriften
def text_with_hover(text: str, hovtxt: str) -> None:  # &#xF505; oder   &#9432
    """css-hack für Überschrift mit mouse-over-tooltip"""
    st.markdown("###")
    st.markdown(
        f"""
        <html>
            <body>
                <span style="{CSS_LABEL_1[1:-1]}; float:left; text-align:left;">
                    <div title="{hovtxt}">
                        {text}
                    </div>
            </body>
        </html>
        """,
        unsafe_allow_html=True,
    )


def widget_headers() -> None:
    """css-hack um die Überschriften von streamlit widgets hübscher zu machen"""
    st.markdown(
        f"""
            <style>
                div.row-widget.stSelectbox > label {CSS_LABEL_1}
                div.row-widget.stMultiSelect > label {CSS_LABEL_1}
                [data-testid='stFileUploader'] > label {CSS_LABEL_1}
                div.streamlit-expanderHeader {CSS_LABEL_2}
            </style>
        """,
        unsafe_allow_html=True,
    )


def color_picker() -> None:
    """Aussehen des color-picker-widgets anpassen"""

    st.markdown(
        """
        <style>
            div.css-1me30nu {           
                gap: 0.5rem;
            }
            div.css-96rroi {
                display: flex; 
                flex-direction: row-reverse; 
                align-items: center; 
                justify-content: flex-end; 
                line-height: 1.6; 
            }
            div.css-96rroi > label {
                margin-bottom: 0px;
                padding-left: 8px;
                font-size: 1rem; 
            } 
            div.css-96rroi > div {
                height: 20px;
                width: 20px;
                vertical-align: middle;
            } 
            div.css-96rroi > div > div {
                height: 20px;
                width: 20px;
                padding: 0px;
                vertical-align: middle;
            } 
        </style>   
        """,
        unsafe_allow_html=True,
    )
