# config_psf.py

# Configure DP83640 PSF operation


def ALP_check():
    Integrity = 0
    try:
        ALPScriptInput
    except:
        Integrity = 1
    return (Integrity)

def GetInput(prompt_string):
    try:
        use_integrity = Integrity
    except:
        use_integrity = 0
    if (use_integrity):
        txt = raw_input(prompt_string)
    else:
        txt = ALPScriptInput(prompt_string)
    return(txt)

#
import sys


#
Integrity = ALP_check()

# ------------------------------------------------------------------
# Default Phy Status Frame Options
cfg.psf_config = PSF_Configuration()
cfg.psf_config.dp83640_mdl_rev = (xem.phyid2 & 0xf)
cfg.psf_config.psf_hdr_data = 0x02ff
cfg.psf_config.psf_mac_sa_sel = 0
cfg.psf_config.psf_ipv4 = 1
cfg.psf_config.psf_ip_src_addr = [0x11, 0x22, 0x33, 0x44]
cfg.psf_config.psf_preamble_len = 7
cfg.psf_config.psf_endian = 0
    
    
# Set PSF Enables
txt = GetInput( "Enable PSF Transmit timestamp (y/n)? ")
txt = txt.strip()   # Remove leading & trailing white space
cfg.psf_config.psf_txts_en = (txt == 'y') | (txt == 'Y')

txt = GetInput( "Enable PSF Receive timestamp (y/n)? ")
txt = txt.strip()   # Remove leading & trailing white space
cfg.psf_config.psf_rxts_en = (txt == 'y') | (txt == 'Y')

txt = GetInput( "Enable PSF Event timestamp (y/n)? ")
txt = txt.strip()   # Remove leading & trailing white space
cfg.psf_config.psf_evnt_en = (txt == 'y') | (txt == 'Y')
    
txt = GetInput( "Enable PSF Trigger status (y/n)? ")
txt = txt.strip()   # Remove leading & trailing white space
cfg.psf_config.psf_trig_en = (txt == 'y') | (txt == 'Y')

