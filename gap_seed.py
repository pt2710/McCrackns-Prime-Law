# gap_seed.py  – one-time helper
# ------------------------------
# Save the 19-gap pattern U1/E1/O1 into seed_gaps.bin

from mccrackns_prime_law import McCracknsPrimeLaw
mpl = McCracknsPrimeLaw(n_primes=20)   # first 19 gaps
mpl.generate()
seed = mpl.get_gaps()                  # includes the leading 1

with open("seed_gaps.bin", "wb") as f:
    import struct
    f.write(struct.pack("<19I", *seed))
print("Wrote 19-gap seed → seed_gaps.bin")
