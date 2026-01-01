import pytest
from src.indicator_manager import IndicatorManager

def test_extract_domain_simple():
    """Vérifie qu'on extrait bien un domaine d'une URL"""
    manager = IndicatorManager()
    content = "Please click on http://malicious-site.com/login to verify account."
    
    indicators = manager.extract_indicators(content)
    
    assert len(indicators) == 1
    assert indicators[0]["type"] == "Domain-Name"
    assert indicators[0]["value"] == "malicious-site.com"

def test_extract_multiple_domains():
    """Vérifie qu'on gère plusieurs domaines sans doublons"""
    manager = IndicatorManager()
    content = "Check http://site1.com and https://site2.org now!"
    
    indicators = manager.extract_indicators(content)
    values = [i["value"] for i in indicators]
    
    assert len(indicators) == 2
    assert "site1.com" in values
    assert "site2.org" in values

def test_no_indicator():
    manager = IndicatorManager()
    content = "Hello world, nothing to see here."
    assert len(manager.extract_indicators(content)) == 0
    
def test_extract_ipv4():
    """Doit détecter une adresse IP valide"""
    manager = IndicatorManager()
    content = "Connect to server at 192.168.1.55 for updates."
    indicators = manager.extract_indicators(content)    
    ips = [i for i in indicators if i["type"] == "IPv4-Addr"]
    
    assert len(ips) == 1
    assert ips[0]["value"] == "192.168.1.55"

def test_extract_hashes():
    """Doit détecter un hash MD5 (32 chars) et SHA256 (64 chars)"""
    manager = IndicatorManager()
    md5_hash = "d41d8cd98f00b204e9800998ecf8427e"
    sha256_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    
    content = f"Malware signatures: {md5_hash} and {sha256_hash}"
    
    indicators = manager.extract_indicators(content)
    values = [i["value"] for i in indicators]
    
    assert md5_hash in values
    assert sha256_hash in values
    
    for i in indicators:
        if i["value"] == md5_hash:
            assert i["type"] == "File-Hash-MD5"