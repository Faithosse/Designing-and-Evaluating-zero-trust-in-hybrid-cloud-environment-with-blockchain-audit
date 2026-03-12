#!/usr/bin/env python3
import json
import time
import hashlib
import os
import sys

CHAIN_FILE = "audit_chain.json"

def sha256(s: str) -> str:
    """Create SHA-256 hash of string"""
    return hashlib.sha256(s.encode()).hexdigest()

def load_chain():
    """Load existing chain or create genesis block"""
    if not os.path.exists(CHAIN_FILE):
        print("Creating genesis block...")
        genesis = {
            "index": 0,
            "timestamp": time.time(),
            "event": {"type": "GENESIS", "description": "Zero Trust Audit Chain Start"},
            "previous_hash": "0" * 64,
            "hash": ""
        }
        # Calculate hash for genesis
        genesis_str = json.dumps({k: v for k, v in genesis.items() if k != "hash"}, sort_keys=True)
        genesis["hash"] = sha256(genesis_str)
        
        with open(CHAIN_FILE, "w") as f:
            json.dump([genesis], f, indent=2)
        print(f"Genesis block created with hash: {genesis['hash'][:16]}...")
    
    with open(CHAIN_FILE, "r") as f:
        return json.load(f)

def append_event(event_dict: dict):
    """Add new audit event to blockchain"""
    chain = load_chain()
    last_block = chain[-1]
    
    # Create new block
    new_block = {
        "index": last_block["index"] + 1,
        "timestamp": time.time(),
        "event": event_dict,
        "previous_hash": last_block["hash"],
        "hash": ""
    }
    
    # Calculate hash (without the hash field itself)
    block_str = json.dumps({k: v for k, v in new_block.items() if k != "hash"}, sort_keys=True)
    new_block["hash"] = sha256(block_str)
    
    # Verify chain integrity before adding
    if not verify_chain(chain):
        print("ERROR: Chain integrity check failed!")
        return False
    
    # Add to chain
    chain.append(new_block)
    
    with open(CHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=2)
    
    print(f"✅ Block #{new_block['index']} added")
    print(f"   Hash: {new_block['hash'][:32]}...")
    print(f"   Previous: {new_block['previous_hash'][:32]}...")
    return True

def verify_chain(chain=None):
    """Verify entire blockchain integrity"""
    if chain is None:
        if not os.path.exists(CHAIN_FILE):
            return True
        with open(CHAIN_FILE, "r") as f:
            chain = json.load(f)
    
    for i in range(1, len(chain)):
        current = chain[i]
        previous = chain[i-1]
        
        # Check hash link
        if current["previous_hash"] != previous["hash"]:
            print(f"❌ Chain broken at block {i}: hash mismatch")
            return False
        
        # Verify current block hash
        block_str = json.dumps({k: v for k, v in current.items() if k != "hash"}, sort_keys=True)
        if sha256(block_str) != current["hash"]:
            print(f"❌ Block {i} hash invalid")
            return False
    
    print(f"✅ Chain verified: {len(chain)} blocks intact")
    return True

def display_chain():
    """Display all blocks in chain"""
    if not os.path.exists(CHAIN_FILE):
        print("No chain found!")
        return
    
    with open(CHAIN_FILE, "r") as f:
        chain = json.load(f)
    
    print(f"\n🔗 Blockchain Audit Trail ({len(chain)} blocks)")
    print("=" * 60)
    
    for block in chain:
        print(f"\nBlock #{block['index']}")
        print(f"  Timestamp: {time.ctime(block['timestamp'])}")
        print(f"  Event: {json.dumps(block['event'], indent=2)}")
        print(f"  Hash: {block['hash'][:40]}...")
        print(f"  Prev: {block['previous_hash'][:40]}...")
        print("-" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"  {sys.argv[0]} add '{{\"type\":\"OPA_DECISION\",\"result\":true,\"user\":\"test\"}}'")
        print(f"  {sys.argv[0]} verify")
        print(f"  {sys.argv[0]} display")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) != 3:
            print("Error: Provide JSON event data")
            sys.exit(1)
        try:
            event = json.loads(sys.argv[2])
            if append_event(event):
                print("Event logged to blockchain")
            else:
                print("Failed to log event")
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}")
            sys.exit(1)
    
    elif command == "verify":
        if verify_chain():
            print("Blockchain integrity verified")
        else:
            print("Blockchain integrity check FAILED")
            sys.exit(1)
    
    elif command == "display":
        display_chain()
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
