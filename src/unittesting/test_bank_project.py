import pytest 
import pandas as pd 
import requests_mock
from src.logging.logger import logger
from src.scraping.bank_project import extract, transform, load_to_csv, load_to_db

def test_extract_happy_path():
    """Test that the extract function returns a valid DataFrame."""
    mock_html = """
    <table>
        <tbody>
            <tr><td>1</td><td><span><a href="#"></span><a href="#" title="Bank Name">Bank Name</a></td><td>Market Cap</td></tr>
            <tr><td>1</td><td><span><a href="#"></span><a href="#" title="Company A">Company A</a></td><td>100.0</td></tr>
            <tr><td>2</td><td><span><a href="#"></span><a href="#" title="Company B">Company B</a></td><td>200.0</td></tr>
            <tr><td>2</td><td><span><a href="#"></span><a href="#" title="Company C">Company C</a></td><td>300.0</td></tr>
        </tbody>
    </table>
    """
    url = "http://example.com"
    table_attribs = ["Name", "MC_USD_Billion"]

    with requests_mock.Mocker() as m:
        m.get(url, text=mock_html)
        df = extract(url, table_attribs)

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == table_attribs
    logger.info(f"Extracted DataFrame: {df}")
    assert df.loc[0, "Name"] == "Company A"
    assert df.loc[0, "MC_USD_Billion"] == "100.0"

def test_extract_malformed_html():
    """Test that extract handles HTML with no tables."""
    mock_html = "<html><body><h1>No Tables Here</h1></body></html>"
    url = "http://example.com"
    table_attribs = ["Name", "MC_USD_Billion"]

    with requests_mock.Mocker() as m:
        m.get(url, text=mock_html)
        df = extract(url, table_attribs)

    assert isinstance(df, pd.DataFrame)
    assert df.empty