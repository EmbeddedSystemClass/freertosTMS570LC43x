
/* constants_dep.h */

#ifndef CONSTANTS_DEP_H
#define CONSTANTS_DEP_H

/**
 *\file
 * \brief Plateform-dependent constants definition
 *
 * This header defines all includes and constants which are plateform-dependent
 *
 */

/* platform dependent */
#define PTPV2_FLAG_OFFSET							6
#define PTPV2_FLAG_LENGTH							2
#define PTPV2_SRC_PORT_ID_OFFSET				28
#define PTPV2_SEQUENCE_ID_OFFSET				30
#define PTPV2_CONTROL_OFFSET					32
#define PTPV2_ORIGIN_TS_SEC_OFFSET			36
#define PTPV2_ORIGIN_TS_NSEC_OFFSET 		40
#define PTPV2_CLOCK_ID_OFFSET 					20
#define PTPV2_CLOCK_ID_LENGTH					8
#define PTPV2_MESSAGE_TYPE_OFFSET			0
#define PTPV2_VERSION_OFFSET						1
#define PTPV2_SUBDOMAIN_OFFSET				4
#define PTPV2_SUBDOMAIN_LENGTH				1
#define PTPV2_MESSAGE_LENGTH_OFFSET		3

#define PTPV2_SYNC_TYPE								0
#define PTPV2_SYNC_CONTROL						0
#define PTPV2_SYNC_LENGTH							0x2C

#define PTPV2_DELAY_REQUEST_TYPE			1
#define PTPV2_DELAY_REQUEST_LENGTH		0x2C
#define PTPV2_DELAY_REQUEST_CONTROL		1

#define PTPV2_DELAY_RESPONSE_TYPE			9
#define PTPV2_DELAY_RESPONSE_CONTROL	3
#define PTPV2_DELAY_RESPONSE_LENGTH		0x36

#define PTPV2_FOLLOWUP_TYPE						8
#define PTPV2_FOLLOWUP_CONTROL				2
#define PTPV2_FOLLOWUP_LENGTH				0x2C

#define IF_NAMESIZE             2
#define INET_ADDRSTRLEN         16

#ifndef TRUE
#define TRUE true
#endif

#ifndef FALSE
#define FALSE false
#endif

#ifndef stdout
#define stdout 1
#endif

#define IFACE_NAME_LENGTH         IF_NAMESIZE
#define NET_ADDRESS_LENGTH        INET_ADDRSTRLEN

#define IFCONF_LENGTH 10

#if BYTE_ORDER == LITTLE_ENDIAN
#define PTPD_LSBF
#elif BYTE_ORDER == BIG_ENDIAN
#define PTPD_MSBF
#endif

/* pow2ms(a) = round(pow(2,a)*1000) */

#define pow2ms(a) (((a)>0) ? (1000 << (a)) : (1000 >>(-(a))))

#define ADJ_FREQ_MAX  512000

/* UDP/IPv4 dependent */

#define SUBDOMAIN_ADDRESS_LENGTH  4
#define PORT_ADDRESS_LENGTH       2
#define PTP_UUID_LENGTH     NETIF_MAX_HWADDR_LEN
#define CLOCK_IDENTITY_LENGTH   8
#define FLAG_FIELD_LENGTH    2

#define PACKET_SIZE  300 /* ptpdv1 value kept because of use of TLV... */

#define PTP_EVENT_PORT    319
#define PTP_GENERAL_PORT  320

#define DEFAULT_PTP_DOMAIN_ADDRESS  "224.0.1.129"
#define PEER_PTP_DOMAIN_ADDRESS     "224.0.0.107"

#define MM_STARTING_BOUNDARY_HOPS  0x7fff

/* Must be a power of 2 */
#define PBUF_QUEUE_SIZE 4
#define PBUF_QUEUE_MASK (PBUF_QUEUE_SIZE - 1)

/* others */

#define SCREEN_BUFSZ  128
#define SCREEN_MAXSZ  80

#endif /* CONSTANTS_DEP_H_*/

