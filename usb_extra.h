
#elif defined(USB_SERIAL_MTP_AUDIO)
  #define VENDOR_ID        0x16C0
  #define PRODUCT_ID       0x048A
  #define MANUFACTURER_NAME    {'T','e','e','n','s','y','d','u','i','n','o'}
  #define MANUFACTURER_NAME_LEN    11
  #define PRODUCT_NAME        {'T','e','e','n','s','y',' ','M','T','P','/','A','u','d','i','o'}
  #define PRODUCT_NAME_LEN    16
  #define EP0_SIZE        64
  #define NUM_ENDPOINTS         7
  #define NUM_INTERFACE        6
  #define CDC_IAD_DESCRIPTOR    1
  #define CDC_STATUS_INTERFACE    0
  #define CDC_DATA_INTERFACE    1    // Serial
  #define CDC_ACM_ENDPOINT    2
  #define CDC_RX_ENDPOINT       3
  #define CDC_TX_ENDPOINT       3
  #define CDC_ACM_SIZE          16
  #define CDC_RX_SIZE_480       512
  #define CDC_TX_SIZE_480       512
  #define CDC_RX_SIZE_12        64
  #define CDC_TX_SIZE_12        64

  #define MTP_INTERFACE        2    // MTP
  #define MTP_TX_ENDPOINT      4
  #define MTP_TX_SIZE_12       64
  #define MTP_TX_SIZE_480      512
  #define MTP_RX_ENDPOINT      4
  #define MTP_RX_SIZE_12       64
  #define MTP_RX_SIZE_480      512
  #define MTP_EVENT_ENDPOINT    7
  #define MTP_EVENT_SIZE    32
  #define MTP_EVENT_INTERVAL_12    10    // 10 = 10 ms
  #define MTP_EVENT_INTERVAL_480 7    // 7 = 8 ms

  #define AUDIO_INTERFACE    3    // Audio (uses 3 consecutive interfaces)
  #define AUDIO_TX_ENDPOINT     5
  #define AUDIO_TX_SIZE         180
  #define AUDIO_RX_ENDPOINT     5
  #define AUDIO_RX_SIZE         180
  #define AUDIO_SYNC_ENDPOINT    6

  #define ENDPOINT2_CONFIG    ENDPOINT_RECEIVE_UNUSED + ENDPOINT_TRANSMIT_INTERRUPT
  #define ENDPOINT3_CONFIG    ENDPOINT_RECEIVE_BULK + ENDPOINT_TRANSMIT_BULK
  #define ENDPOINT4_CONFIG    ENDPOINT_RECEIVE_BULK + ENDPOINT_TRANSMIT_BULK
  #define ENDPOINT5_CONFIG    ENDPOINT_RECEIVE_ISOCHRONOUS + ENDPOINT_TRANSMIT_ISOCHRONOUS
  #define ENDPOINT6_CONFIG    ENDPOINT_RECEIVE_UNUSED + ENDPOINT_TRANSMIT_ISOCHRONOUS
  #define ENDPOINT7_CONFIG    ENDPOINT_RECEIVE_UNUSED + ENDPOINT_TRANSMIT_INTERRUPT
  
#elif defined(USB_MTP_AUDIO_MIDI)
  #define VENDOR_ID        0x16C0
  #define PRODUCT_ID       0x04D1
  #define BCD_DEVICE		 0x0210
  #define MANUFACTURER_NAME    {'T','e','e','n','s','y','d','u','i','n','o'}
  #define MANUFACTURER_NAME_LEN    11
  #define PRODUCT_NAME        {'T','e','e','n','s','y',' ','M','T','P','/','A','u','d','i','o','/','M','I','D','I'}
  #define PRODUCT_NAME_LEN    21
  #define EP0_SIZE            64
  #define NUM_ENDPOINTS          7
  #define NUM_INTERFACE         6

  #define SEREMU_INTERFACE      0	// Serial emulation
  #define SEREMU_TX_ENDPOINT     2
  #define SEREMU_TX_SIZE          64
  #define SEREMU_TX_INTERVAL      1
  #define SEREMU_RX_ENDPOINT     2
  #define SEREMU_RX_SIZE          32
  #define SEREMU_RX_INTERVAL      2

  #define MTP_INTERFACE        1    // MTP
  #define MTP_TX_ENDPOINT       3
  #define MTP_TX_SIZE_12         64
  #define MTP_TX_SIZE_480        512
  #define MTP_RX_ENDPOINT       3
  #define MTP_RX_SIZE_12         64
  #define MTP_RX_SIZE_480        512
  #define MTP_EVENT_ENDPOINT    4
  #define MTP_EVENT_SIZE         32
  #define MTP_EVENT_INTERVAL_12  10    // 10 = 10 ms
  #define MTP_EVENT_INTERVAL_480 7    // 7 = 8 ms

  #define MIDI_INTERFACE       2	// MIDI
  #define MIDI_NUM_CABLES        1
  #define MIDI_TX_ENDPOINT      5
  #define MIDI_TX_SIZE_12        64
  #define MIDI_TX_SIZE_480       512
  #define MIDI_RX_ENDPOINT      5
  #define MIDI_RX_SIZE_12        64
  #define MIDI_RX_SIZE_480       512

  #define AUDIO_INTERFACE      3    // Audio (uses 3 consecutive interfaces)
  #define AUDIO_TX_ENDPOINT     6
  #define AUDIO_TX_SIZE          180
  #define AUDIO_RX_ENDPOINT     6
  #define AUDIO_RX_SIZE          180
  #define AUDIO_SYNC_ENDPOINT   7

  #define ENDPOINT2_CONFIG	ENDPOINT_RECEIVE_INTERRUPT + ENDPOINT_TRANSMIT_INTERRUPT // Serial emulation
  #define ENDPOINT3_CONFIG    ENDPOINT_RECEIVE_BULK + ENDPOINT_TRANSMIT_BULK // MTP TX/RX
  #define ENDPOINT4_CONFIG    ENDPOINT_RECEIVE_UNUSED + ENDPOINT_TRANSMIT_INTERRUPT  // MTP event
  #define ENDPOINT5_CONFIG    ENDPOINT_RECEIVE_BULK + ENDPOINT_TRANSMIT_BULK // MIDI
  #define ENDPOINT6_CONFIG    ENDPOINT_RECEIVE_ISOCHRONOUS + ENDPOINT_TRANSMIT_ISOCHRONOUS // Audio TX/RX
  #define ENDPOINT7_CONFIG    ENDPOINT_RECEIVE_UNUSED + ENDPOINT_TRANSMIT_ISOCHRONOUS // Audio sync
  