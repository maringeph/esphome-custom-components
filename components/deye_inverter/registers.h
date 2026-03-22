#pragma once

#include <cstdint>

namespace esphome {
namespace deye_inverter {

// =============================================================================
// DEVICE INFO REGISTERS (30 registers: 0-29)
// =============================================================================

constexpr uint16_t REG_DEVICE_TYPE = 0;           // Gerätetyp
constexpr uint16_t REG_MODBUS_ADDRESS = 1;        // Modbus Adresse

// Serial Number and Communication Protocol (2-29)
constexpr uint16_t REG_COMM_PROTOCOL_VERSION = 2; // Kommunikationsprotokoll-Version
constexpr uint16_t REG_SERIAL_NUMBER_01 = 3;      // Seriennummer Byte 01
constexpr uint16_t REG_SERIAL_NUMBER_03 = 4;      // Seriennummer Byte 03
constexpr uint16_t REG_SERIAL_NUMBER_05 = 5;      // Seriennummer Byte 05
constexpr uint16_t REG_SERIAL_NUMBER_07 = 6;      // Seriennummer Byte 07
constexpr uint16_t REG_SERIAL_NUMBER_09 = 7;      // Seriennummer Byte 09
constexpr uint16_t REG_POWER_LEVEL = 8;           // Leistungsstufe
constexpr uint16_t REG_RESERVED_9 = 9;            // Reserviert 9
constexpr uint16_t REG_RESERVED_10 = 10;          // Reserviert 10
constexpr uint16_t REG_CONTROL_BOARD_FIRMWARE = 11;    // Steuerplatine Firmware
constexpr uint16_t REG_RESERVED_12 = 12;          // Reserviert 12
constexpr uint16_t REG_RESERVED_13 = 13;          // Reserviert 13
constexpr uint16_t REG_CONTROL_BOARD_FIRMWARE_PART2 = 14;  // Steuerplatine Firmware Teil 2
constexpr uint16_t REG_CONTROL_BOARD_FIRMWARE_VERSION = 15; // Steuerplatine Firmware Version
constexpr uint16_t REG_COMM_BOARD_FIRMWARE_PART1 = 16;  // Kommunikationsplatine Firmware Teil 1
constexpr uint16_t REG_COMM_BOARD_FIRMWARE_PART2 = 17;  // Kommunikationsplatine Firmware Teil 2
constexpr uint16_t REG_COMM_BOARD_FIRMWARE_VERSION = 18; // Kommunikationsplatine Firmware Version
constexpr uint16_t REG_SAFETY_REGULATION_TYPE = 19; // Sicherheitsnorm-Typ
constexpr uint16_t REG_RATED_POWER_LOW = 20;      // Nennleistung niedrig
constexpr uint16_t REG_RATED_POWER_HIGH = 21;     // Nennleistung hoch
constexpr uint16_t REG_MPPT_COUNT_AND_PHASES = 22; // MPPT Anzahl und Phasen
constexpr uint16_t REG_RATED_GRID_VOLTAGE = 23;   // Nenn-Netzspannung
constexpr uint16_t REG_RESERVED_24 = 24;          // Reserviert 24
constexpr uint16_t REG_RESERVED_SN_01 = 25;       // Reserviert SN Byte 01
constexpr uint16_t REG_RESERVED_SN_03 = 26;       // Reserviert SN Byte 03
constexpr uint16_t REG_RESERVED_SN_05 = 27;       // Reserviert SN Byte 05
constexpr uint16_t REG_RESERVED_SN_07 = 28;       // Reserviert SN Byte 07
constexpr uint16_t REG_RESERVED_SN_09 = 29;       // Reserviert SN Byte 09

// =============================================================================
// SYSTEM SETTINGS REGISTERS (32 registers: 60-97)
// =============================================================================

constexpr uint16_t REG_REMOTE_CONTROL_ENABLE = 60;    // Fernsteuerung Aktivierung
constexpr uint16_t REG_BOOT_SELF_CHECK_TIME = 61;     // Boot Selbsttest-Zeit
constexpr uint16_t REG_SYSTEM_TIME_BYTE1 = 62;        // Systemzeit Byte 1
constexpr uint16_t REG_SYSTEM_TIME_BYTE3 = 63;        // Systemzeit Byte 3
constexpr uint16_t REG_SYSTEM_TIME_BYTE5 = 64;        // Systemzeit Byte 5
constexpr uint16_t REG_INSULATION_RESISTANCE_LIMIT = 65; // Isolationswiderstand-Limit
constexpr uint16_t REG_RESERVED_66 = 66;              // Reserviert 66
constexpr uint16_t REG_RESERVED_67 = 67;              // Reserviert 67
constexpr uint16_t REG_RESERVED_68 = 68;              // Reserviert 68
constexpr uint16_t REG_RESERVED_69 = 69;              // Reserviert 69
constexpr uint16_t REG_RESERVED_70 = 70;              // Reserviert 70
constexpr uint16_t REG_RESERVED_71 = 71;              // Reserviert 71
constexpr uint16_t REG_RESERVED_72 = 72;              // Reserviert 72
constexpr uint16_t REG_RESERVED_73 = 73;              // Reserviert 73
constexpr uint16_t REG_MODBUS_ADDRESS_SETTING = 74;   // Modbus-Adresse Einstellung
constexpr uint16_t REG_BAUD_RATE = 75;                // Baudrate
constexpr uint16_t REG_RESERVED_76 = 76;              // Reserviert 76
constexpr uint16_t REG_ACTIVE_POWER_REGULATION = 77;  // Wirkleistungsregelung
constexpr uint16_t REG_REACTIVE_POWER_REGULATION = 78; // Blindleistungsregelung
constexpr uint16_t REG_APPARENT_POWER_REGULATION = 79; // Scheinleistungsregelung
constexpr uint16_t REG_RESERVED_80 = 80;              // Reserviert 80
constexpr uint16_t REG_FACTORY_RESET_ENABLE = 81;     // Werksreset Aktivierung
constexpr uint16_t REG_SELF_CHECK_TIME = 82;          // Selbsttest-Zeit
constexpr uint16_t REG_ISLAND_PROTECTION_ENABLE = 83; // Insel-Schutz Aktivierung
constexpr uint16_t REG_MPPT_NUMBER = 84;              // MPPT Anzahl
constexpr uint16_t REG_GFDI_ENABLE = 85;              // GFDI Aktivierung
constexpr uint16_t REG_RESERVED_86 = 86;              // Reserviert 86
constexpr uint16_t REG_RISO_ENABLE = 87;              // RISO Aktivierung
constexpr uint16_t REG_RESERVED_88 = 88;              // Reserviert 88
constexpr uint16_t REG_RESERVED_89 = 89;              // Reserviert 89
constexpr uint16_t REG_VOLTAGE_RIDE_THROUGH_ENABLE = 90; // Spannungsdurchgriff-Aktivierung
constexpr uint16_t REG_CONTROL_BOARD_EEPROM_INIT = 91;   // Steuerplatine EEPROM Initialisierung
constexpr uint16_t REG_COMM_BOARD_EEPROM_INIT = 92;      // Kommunikationsplatine EEPROM Initialisierung
constexpr uint16_t REG_RESERVED_93 = 93;              // Reserviert 93
constexpr uint16_t REG_RESERVED_94 = 94;              // Reserviert 94
constexpr uint16_t REG_RESERVED_95 = 95;              // Reserviert 95
constexpr uint16_t REG_GENERATION_CORRECTION_FACTOR = 96; // Erzeugungskorrekturfaktor
constexpr uint16_t REG_SOLAR_INPUT_SPU = 97;          // Solar-Eingang SPU

// =============================================================================
// GRID PROTECTION AND PEAK SHAVING SETTINGS (16 registers: 185-200)
// =============================================================================

constexpr uint16_t REG_GRID_OVERVOLTAGE_PROTECTION = 185;  // Netz-Überspannungsschutz
constexpr uint16_t REG_GRID_UNDERVOLTAGE_PROTECTION = 186; // Netz-Unterspannungsschutz
constexpr uint16_t REG_GRID_OVERFREQ_PROTECTION = 187;     // Netz-Überfrequenzschutz
constexpr uint16_t REG_GRID_UNDERFREQ_PROTECTION = 188;    // Netz-Unterfrequenzschutz
constexpr uint16_t REG_GEN_CONNECT_TO_GRID_INPUT = 189;    // Generator an Netz-Eingang
constexpr uint16_t REG_GEN_PEAK_SHAVING_POWER = 190;       // Generator Peak Shaving Leistung
constexpr uint16_t REG_GRID_PEAK_SHAVING_POWER = 191;      // Netz Peak Shaving Leistung
constexpr uint16_t REG_SMART_LOAD_OPEN_DELAY = 192;        // Smart Load Öffnungs-Verzögerung
constexpr uint16_t REG_OUTPUT_PF_SETTING = 193;            // Ausgangs-PF-Einstellung
constexpr uint16_t REG_EXTERNAL_RELAY_FUNCTION = 194;      // Externes Relais Funktion
constexpr uint16_t REG_ARC_FACTORY_B_HIGH_FREQ = 195;      // ARC Factory B hohe Frequenz
constexpr uint16_t REG_ARC_FACTORY_B_LOW_FREQ = 196;       // ARC Factory B niedrige Frequenz
constexpr uint16_t REG_ARC_FACTORY_I_HIGH_CURRENT = 197;   // ARC Factory I hoher Strom
constexpr uint16_t REG_ARC_FACTORY_I_LOW_CURRENT = 198;    // ARC Factory I niedriger Strom
constexpr uint16_t REG_ARC_FACTORY_F_HIGH_FREQ = 199;      // ARC Factory F hohe Frequenz
constexpr uint16_t REG_ARC_FACTORY_F_LOW_FREQ = 200;       // ARC Factory F niedrige Frequenz

// =============================================================================
// EXTENDED MONITORING AND WIND INPUT SETTINGS (47 registers: 231-339)
// =============================================================================

constexpr uint16_t REG_FACTORY_TEST_PROGRAM = 240;    // Werksseitiges Testprogramm

// Grid and Inverter Monitoring (269-289)
constexpr uint16_t REG_GRID1_CURRENT = 269;           // Netz 1 Strom
constexpr uint16_t REG_GRID2_CURRENT = 270;           // Netz 2 Strom
constexpr uint16_t REG_GRID3_CURRENT = 271;           // Netz 3 Strom
constexpr uint16_t REG_GRID_VOLTAGE_L1_MONITOR = 272; // Netzspannung L1 Überwachung
constexpr uint16_t REG_GRID_VOLTAGE_L2_MONITOR = 273; // Netzspannung L2 Überwachung
constexpr uint16_t REG_GRID_VOLTAGE_L3_MONITOR = 274; // Netzspannung L3 Überwachung
constexpr uint16_t REG_LIMIT1_CURRENT = 275;          // Limit 1 Strom
constexpr uint16_t REG_LIMIT2_CURRENT = 276;          // Limit 2 Strom
constexpr uint16_t REG_LIMIT3_CURRENT = 277;          // Limit 3 Strom
constexpr uint16_t REG_PV1_VOLTAGE_MONITOR = 278;     // PV1 Spannung Überwachung
constexpr uint16_t REG_PV1_CURRENT_MONITOR = 279;     // PV1 Strom Überwachung
constexpr uint16_t REG_PV2_VOLTAGE_MONITOR = 280;     // PV2 Spannung Überwachung
constexpr uint16_t REG_PV2_CURRENT_MONITOR = 281;     // PV2 Strom Überwachung
constexpr uint16_t REG_INV_A_CURRENT = 282;           // Wechselrichter A Strom
constexpr uint16_t REG_INV_B_CURRENT = 283;           // Wechselrichter B Strom
constexpr uint16_t REG_INV_C_CURRENT = 284;           // Wechselrichter C Strom
constexpr uint16_t REG_INV_A_VOLTAGE = 285;           // Wechselrichter A Spannung
constexpr uint16_t REG_INV_B_VOLTAGE = 286;           // Wechselrichter B Spannung
constexpr uint16_t REG_INV_C_VOLTAGE = 287;           // Wechselrichter C Spannung
constexpr uint16_t REG_BAT_CURRENT_MONITOR = 288;     // Batterie Strom Überwachung
constexpr uint16_t REG_BAT_VOLTAGE_MONITOR = 289;     // Batterie Spannung Überwachung

// Wind Input Settings (310-339)
constexpr uint16_t REG_SOLAR_AS_WIND_INPUT_ENABLE = 310; // Solar als Wind-Eingang Aktivierung
constexpr uint16_t REG_VOLTAGE_311 = 311;             // Spannung 311
constexpr uint16_t REG_VOLTAGE_312 = 312;             // Spannung 312
constexpr uint16_t REG_VOLTAGE_313 = 313;             // Spannung 313
constexpr uint16_t REG_VOLTAGE_314 = 314;             // Spannung 314
constexpr uint16_t REG_VOLTAGE_315 = 315;             // Spannung 315
constexpr uint16_t REG_VOLTAGE_316 = 316;             // Spannung 316
constexpr uint16_t REG_VOLTAGE_317 = 317;             // Spannung 317
constexpr uint16_t REG_VOLTAGE_318 = 318;             // Spannung 318
constexpr uint16_t REG_VOLTAGE_319 = 319;             // Spannung 319
constexpr uint16_t REG_VOLTAGE_320 = 320;             // Spannung 320
constexpr uint16_t REG_VOLTAGE_321 = 321;             // Spannung 321
constexpr uint16_t REG_VOLTAGE_322 = 322;             // Spannung 322
constexpr uint16_t REG_CURRENT_323 = 323;             // Strom 323
constexpr uint16_t REG_CURRENT_324 = 324;             // Strom 324
constexpr uint16_t REG_CURRENT_325 = 325;             // Strom 325
constexpr uint16_t REG_CURRENT_326 = 326;             // Strom 326
constexpr uint16_t REG_CURRENT_327 = 327;             // Strom 327
constexpr uint16_t REG_CURRENT_328 = 328;             // Strom 328
constexpr uint16_t REG_CURRENT_329 = 329;             // Strom 329
constexpr uint16_t REG_CURRENT_330 = 330;             // Strom 330
constexpr uint16_t REG_CURRENT_331 = 331;             // Strom 331
constexpr uint16_t REG_CURRENT_332 = 332;             // Strom 332
constexpr uint16_t REG_CURRENT_333 = 333;             // Strom 333
constexpr uint16_t REG_CURRENT_334 = 334;             // Strom 334
constexpr uint16_t REG_RESERVED_335 = 335;            // Reserviert 335
constexpr uint16_t REG_PARALLEL1 = 336;               // Parallel 1
constexpr uint16_t REG_PARALLEL2 = 337;               // Parallel 2
constexpr uint16_t REG_RESERVED_338 = 338;            // Reserviert 338
constexpr uint16_t REG_RESERVED_339 = 339;            // Reserviert 339

// =============================================================================
// CALIFORNIA COMPLIANCE AND ADVANCED SETTINGS (49 registers: 341-419)
// =============================================================================

constexpr uint16_t REG_RESERVED_341 = 341;            // Reserviert 341
constexpr uint16_t REG_RESERVED_342 = 342;            // Reserviert 342
constexpr uint16_t REG_RESERVED_343 = 343;            // Reserviert 343
constexpr uint16_t REG_GRID_MONITORING_METHOD = 344;  // Netz-Überwachungsmethode
constexpr uint16_t REG_RESERVED_345 = 345;            // Reserviert 345
constexpr uint16_t REG_RESERVED_346 = 346;            // Reserviert 346
constexpr uint16_t REG_EXTERNAL_CT_RATIO = 347;       // Externer CT-Verhältnis
constexpr uint16_t REG_METER_CT_RATIO = 348;          // Zähler CT-Verhältnis
constexpr uint16_t REG_RESERVED_349 = 349;            // Reserviert 349
constexpr uint16_t REG_CHARGE_RAMP_CONTROL_1 = 350;   // Lade-Rampensteuerung 1
constexpr uint16_t REG_CHARGE_RAMP_CONTROL_2 = 351;   // Lade-Rampensteuerung 2
constexpr uint16_t REG_RESERVED_352 = 352;            // Reserviert 352
constexpr uint16_t REG_RESERVED_353 = 353;            // Reserviert 353
constexpr uint16_t REG_RESERVED_354 = 354;            // Reserviert 354
constexpr uint16_t REG_RESERVED_355 = 355;            // Reserviert 355
constexpr uint16_t REG_RESERVED_356 = 356;            // Reserviert 356
constexpr uint16_t REG_RESERVED_357 = 357;            // Reserviert 357
constexpr uint16_t REG_RESERVED_358 = 358;            // Reserviert 358
constexpr uint16_t REG_OFFGRID_UNDERVOLTAGE_180V = 359; // Off-Grid Unterspannung 180V

// California LHVRT Settings (380-390)
constexpr uint16_t REG_CA_LHVRT_ENABLE = 380;         // CA LHVRT Aktivierung
constexpr uint16_t REG_CA_HV2 = 381;                  // CA HV2
constexpr uint16_t REG_CA_HV1 = 382;                  // CA HV1
constexpr uint16_t REG_CA_LV1 = 383;                  // CA LV1
constexpr uint16_t REG_CA_LV2 = 384;                  // CA LV2
constexpr uint16_t REG_CA_LV3 = 385;                  // CA LV3
constexpr uint16_t REG_CA_HV2_TIME = 386;             // CA HV2 Zeit
constexpr uint16_t REG_CA_HV1_TIME = 387;             // CA HV1 Zeit
constexpr uint16_t REG_CA_LV1_TIME = 388;             // CA LV1 Zeit
constexpr uint16_t REG_CA_LV2_TIME = 389;             // CA LV2 Zeit
constexpr uint16_t REG_CA_LV3_TIME = 390;             // CA LV3 Zeit

// California LHFRT Settings (391-399)
constexpr uint16_t REG_CA_LHFRT_ENABLE = 391;         // CA LHFRT Aktivierung
constexpr uint16_t REG_CA_HF2 = 392;                  // CA HF2
constexpr uint16_t REG_CA_HF1 = 393;                  // CA HF1
constexpr uint16_t REG_CA_LF1 = 394;                  // CA LF1
constexpr uint16_t REG_CA_LF2 = 395;                  // CA LF2
constexpr uint16_t REG_CA_HF2_TIME = 396;             // CA HF2 Zeit
constexpr uint16_t REG_CA_HF1_TIME = 397;             // CA HF1 Zeit
constexpr uint16_t REG_CA_LF1_TIME = 398;             // CA LF1 Zeit
constexpr uint16_t REG_CA_LF2_TIME = 399;             // CA LF2 Zeit

// California QV Settings (400-408)
constexpr uint16_t REG_CA_QV_ENABLE = 400;            // CA QV Aktivierung
constexpr uint16_t REG_CA_QV_V1 = 401;                // CA QV V1
constexpr uint16_t REG_CA_QV_V2 = 402;                // CA QV V2
constexpr uint16_t REG_CA_QV_V3 = 403;                // CA QV V3
constexpr uint16_t REG_CA_QV_V4 = 404;                // CA QV V4
constexpr uint16_t REG_CA_QV_Q1 = 405;                // CA QV Q1
constexpr uint16_t REG_CA_QV_Q2 = 406;                // CA QV Q2
constexpr uint16_t REG_CA_QV_Q3 = 407;                // CA QV Q3
constexpr uint16_t REG_CA_QV_Q4 = 408;                // CA QV Q4

// California FW and VW Settings (409-418)
constexpr uint16_t REG_CA_FW_ENABLE = 409;            // CA FW Aktivierung
constexpr uint16_t REG_CA_FSTART = 410;               // CA Fstart
constexpr uint16_t REG_CA_FSTOP = 411;                // CA Fstop
constexpr uint16_t REG_CA_VW_ENABLE = 412;            // CA VW Aktivierung
constexpr uint16_t REG_CA_VSTART = 413;               // CA Vstart
constexpr uint16_t REG_CA_VSTOP = 414;                // CA Vstop
constexpr uint16_t REG_NORMAL_START_RAMP_RATE = 415;  // Normaler Start-Rampenrate
constexpr uint16_t REG_SOFT_START_RAMP_RATE = 416;    // Soft-Start-Rampenrate
constexpr uint16_t REG_QV_RESPONSE_TIME = 417;        // QV Reaktionszeit
constexpr uint16_t REG_VW_RESPONSE_TIME = 418;        // VW Reaktionszeit
constexpr uint16_t REG_FW_RESPONSE_TIME = 419;        // FW Reaktionszeit

// =============================================================================
// SETTINGS REGISTERS (107 registers: 98-230, 340)
// =============================================================================

// Battery Settings (98-120)
constexpr uint16_t REG_BATTERY_TYPE = 98;                    // Batterietyp
constexpr uint16_t REG_BATTERY_EQUALIZATION_VOLTAGE = 99;    // Batterie-Ausgleichsspannung
constexpr uint16_t REG_BATTERY_ABSORPTION_VOLTAGE = 100;     // Batterie-Absorptionsspannung
constexpr uint16_t REG_BATTERY_FLOAT_VOLTAGE = 101;          // Batterie-Float-Spannung
constexpr uint16_t REG_BATTERY_CAPACITY = 102;               // Batterie-Kapazität (Ah)
constexpr uint16_t REG_BATTERY_EMPTY_VOLTAGE = 103;          // Leer-Spannung
constexpr uint16_t REG_ZERO_EXPORT_POWER = 104;              // Zero-Export-Leistung (%)
constexpr uint16_t REG_BATTERY_EQUALIZATION_DAY_CYCLE = 105; // Ausgleichszyklus (Tage)
constexpr uint16_t REG_BATTERY_EQUALIZATION_TIME = 106;      // Ausgleichszeit (h)
constexpr uint16_t REG_BATTERY_TEMPCO = 107;                 // Temperaturkompensation (mV/°C)
constexpr uint16_t REG_BATTERY_MAX_CHARGE_CURRENT = 108;     // Maximaler Lade-Strom (A)
constexpr uint16_t REG_BATTERY_MAX_DISCHARGE_CURRENT = 109;  // Maximaler Entlade-Strom (A)
constexpr uint16_t REG_RESERVE_110 = 110;                    // Reserve 110
constexpr uint16_t REG_BATTERY_CONTROL_MODE = 111;           // Batterie-Steuerungsmodus
constexpr uint16_t REG_BATTERY_WAKE_UP = 112;                // Batterie-Aufwecksignal
constexpr uint16_t REG_BATTERY_RESISTANCE = 113;             // Batterie-Innenwiderstand (mΩ)
constexpr uint16_t REG_BATTERY_CHARGING_EFFICIENCY = 114;    // Batterie-Ladeeffizienz (%)
constexpr uint16_t REG_BATTERY_SHUTDOWN_SOC = 115;           // Abschaltung SOC (%)
constexpr uint16_t REG_BATTERY_RESTART_SOC = 116;            // Neustart SOC (%)
constexpr uint16_t REG_BATTERY_LOW_SOC_WARNING = 117;        // Niedrig-SOC Warnung (%)
constexpr uint16_t REG_BATTERY_SHUTDOWN_VOLTAGE = 118;       // Abschaltspannung (V)
constexpr uint16_t REG_BATTERY_RESTART_VOLTAGE = 119;        // Neustartspannung (V)
constexpr uint16_t REG_BATTERY_LOW_VOLTAGE_WARNING = 120;    // Niedrigspannungs-Warnung (V)

// Generator Settings (121-127)
constexpr uint16_t REG_GENERATOR_MAX_RUN_TIME = 121;         // Generator Max-Laufzeit (h)
constexpr uint16_t REG_GENERATOR_COOLDOWN_TIME = 122;        // Generator Kühlzeit (min)
constexpr uint16_t REG_GENERATOR_MIN_POWER = 123;            // Generator Mindestleistung (W)
constexpr uint16_t REG_GENERATOR_START_VOLTAGE = 124;        // Generator Start-Spannung (V)
constexpr uint16_t REG_GENERATOR_START_SOC = 125;            // Generator Start-SOC (%)
constexpr uint16_t REG_GENERATOR_CHARGE_CURRENT = 126;       // Generator Ladestrom (A)
constexpr uint16_t REG_GENERATOR_ENABLE = 127;               // Generator Aktivierung

// Grid/Port Settings (128-147)
constexpr uint16_t REG_MAX_BATTERY_GRID_CHARGE_CURRENT = 128;    // Maximaler Batterie-Netz-Ladestrom (A)
constexpr uint16_t REG_GENERATOR_CHARGING_ENABLED = 129;         // Generator-Ladung aktiviert
constexpr uint16_t REG_GRID_CHARGE = 130;                        // Netz-Ladung
constexpr uint16_t REG_GEN_PORT_COUPLE_FREQUENCY = 131;          // Gen Port Kopplungsfrequenz-Limit (Hz)
constexpr uint16_t REG_GEN_PORT_FORCE_ON = 132;                  // Gen Port Force On
constexpr uint16_t REG_GEN_PORT_CONTROL_MODE = 133;              // Generator-Port Steuerungsmodus
constexpr uint16_t REG_SMART_LOAD_OFF_VOLTAGE = 134;             // Smart Load Aus-Spannung (V)
constexpr uint16_t REG_SMART_LOAD_OFF_CAPACITY_SOC = 135;        // Smart Load Aus-Kapazität SOC (%)
constexpr uint16_t REG_SMART_LOAD_ON_VOLTAGE = 136;              // Smart Load Ein-Spannung (V)
constexpr uint16_t REG_SMART_LOAD_ON_CAPACITY_SOC = 137;         // Smart Load Ein-Kapazität SOC (%)
constexpr uint16_t REG_GRID_NOMINAL_VOLTAGE = 138;               // Netz-Nennspannung
constexpr uint16_t REG_GENERATOR_REQUIRED_POWER_START = 139;     // Generator Erforderliche Startleistung (W)
constexpr uint16_t REG_GENERATOR_UNKNOWN_140 = 140;              // Generator Unbekannt 140
constexpr uint16_t REG_ENERGY_PRIORITY = 141;                    // Energie-Priorität
constexpr uint16_t REG_LIMIT_CONTROL_MODE = 142;                 // Begrenzungs-Kontrollmodus
constexpr uint16_t REG_MAX_SOLAR_SELL_POWER = 143;               // Max Solar-Verkaufsleistung (W)
constexpr uint16_t REG_GRID_UNKNOWN_144 = 144;                   // Netz Unbekannt 144
constexpr uint16_t REG_SOLAR_SELL = 145;                         // Solar-Verkauf
constexpr uint16_t REG_TIME_OF_USE = 146;                        // Zeitgesteuerte Nutzung
constexpr uint16_t REG_GRID_PHASE_SEQUENCE = 147;                // Netz-Phasenfolge

// Time Point Settings (148-177)
// Start Times
constexpr uint16_t REG_TIME_POINT_1_START = 148;             // Zeitpunkt 1 Start (HHMM)
constexpr uint16_t REG_TIME_POINT_2_START = 149;             // Zeitpunkt 2 Start (HHMM)
constexpr uint16_t REG_TIME_POINT_3_START = 150;             // Zeitpunkt 3 Start (HHMM)
constexpr uint16_t REG_TIME_POINT_4_START = 151;             // Zeitpunkt 4 Start (HHMM)
constexpr uint16_t REG_TIME_POINT_5_START = 152;             // Zeitpunkt 5 Start (HHMM)
constexpr uint16_t REG_TIME_POINT_6_START = 153;             // Zeitpunkt 6 Start (HHMM)
// Power Settings
constexpr uint16_t REG_TIME_POINT_1_POWER = 154;             // Zeitpunkt 1 Leistung (W)
constexpr uint16_t REG_TIME_POINT_2_POWER = 155;             // Zeitpunkt 2 Leistung (W)
constexpr uint16_t REG_TIME_POINT_3_POWER = 156;             // Zeitpunkt 3 Leistung (W)
constexpr uint16_t REG_TIME_POINT_4_POWER = 157;             // Zeitpunkt 4 Leistung (W)
constexpr uint16_t REG_TIME_POINT_5_POWER = 158;             // Zeitpunkt 5 Leistung (W)
constexpr uint16_t REG_TIME_POINT_6_POWER = 159;             // Zeitpunkt 6 Leistung (W)
// Min Battery Voltage
constexpr uint16_t REG_TIME_POINT_1_MIN_VOLTAGE = 160;       // Zeitpunkt 1 Min. Batteriespannung (V)
constexpr uint16_t REG_TIME_POINT_2_MIN_VOLTAGE = 161;       // Zeitpunkt 2 Min. Batteriespannung (V)
constexpr uint16_t REG_TIME_POINT_3_MIN_VOLTAGE = 162;       // Zeitpunkt 3 Min. Batteriespannung (V)
constexpr uint16_t REG_TIME_POINT_4_MIN_VOLTAGE = 163;       // Zeitpunkt 4 Min. Batteriespannung (V)
constexpr uint16_t REG_TIME_POINT_5_MIN_VOLTAGE = 164;       // Zeitpunkt 5 Min. Batteriespannung (V)
constexpr uint16_t REG_TIME_POINT_6_MIN_VOLTAGE = 165;       // Zeitpunkt 6 Min. Batteriespannung (V)
// Capacity Settings
constexpr uint16_t REG_TIME_POINT_1_CAPACITY = 166;          // Zeitpunkt 1 Kapazität (%)
constexpr uint16_t REG_TIME_POINT_2_CAPACITY = 167;          // Zeitpunkt 2 Kapazität (%)
constexpr uint16_t REG_TIME_POINT_3_CAPACITY = 168;          // Zeitpunkt 3 Kapazität (%)
constexpr uint16_t REG_TIME_POINT_4_CAPACITY = 169;          // Zeitpunkt 4 Kapazität (%)
constexpr uint16_t REG_TIME_POINT_5_CAPACITY = 170;          // Zeitpunkt 5 Kapazität (%)
constexpr uint16_t REG_TIME_POINT_6_CAPACITY = 171;          // Zeitpunkt 6 Kapazität (%)
// Charge Enable (Solar/General - Bit 0)
constexpr uint16_t REG_TIME_POINT_1_CHARGE_ENABLE = 172;     // Zeitpunkt 1 Ladefreigabe (Bit 0)
constexpr uint16_t REG_TIME_POINT_2_CHARGE_ENABLE = 173;     // Zeitpunkt 2 Ladefreigabe (Bit 0)
constexpr uint16_t REG_TIME_POINT_3_CHARGE_ENABLE = 174;     // Zeitpunkt 3 Ladefreigabe (Bit 0)
constexpr uint16_t REG_TIME_POINT_4_CHARGE_ENABLE = 175;     // Zeitpunkt 4 Ladefreigabe (Bit 0)
constexpr uint16_t REG_TIME_POINT_5_CHARGE_ENABLE = 176;     // Zeitpunkt 5 Ladefreigabe (Bit 0)
constexpr uint16_t REG_TIME_POINT_6_CHARGE_ENABLE = 177;     // Zeitpunkt 6 Ladefreigabe (Bit 0)

// Grid Charge Enable (Bit 1) - Same registers, different bit
constexpr uint16_t REG_TIME_POINT_1_GRID_CHARGE_ENABLE = 172;  // Zeitpunkt 1 Grid Ladung (Bit 1)
constexpr uint16_t REG_TIME_POINT_2_GRID_CHARGE_ENABLE = 173;  // Zeitpunkt 2 Grid Ladung (Bit 1)
constexpr uint16_t REG_TIME_POINT_3_GRID_CHARGE_ENABLE = 174;  // Zeitpunkt 3 Grid Ladung (Bit 1)
constexpr uint16_t REG_TIME_POINT_4_GRID_CHARGE_ENABLE = 175;  // Zeitpunkt 4 Grid Ladung (Bit 1)
constexpr uint16_t REG_TIME_POINT_5_GRID_CHARGE_ENABLE = 176;  // Zeitpunkt 5 Grid Ladung (Bit 1)
constexpr uint16_t REG_TIME_POINT_6_GRID_CHARGE_ENABLE = 177;  // Zeitpunkt 6 Grid Ladung (Bit 1)

// Generator Charge Enable (Bit 2) - Same registers, different bit
constexpr uint16_t REG_TIME_POINT_1_GEN_CHARGE_ENABLE = 172;   // Zeitpunkt 1 Generator Ladung (Bit 2)
constexpr uint16_t REG_TIME_POINT_2_GEN_CHARGE_ENABLE = 173;   // Zeitpunkt 2 Generator Ladung (Bit 2)
constexpr uint16_t REG_TIME_POINT_3_GEN_CHARGE_ENABLE = 174;   // Zeitpunkt 3 Generator Ladung (Bit 2)
constexpr uint16_t REG_TIME_POINT_4_GEN_CHARGE_ENABLE = 175;   // Zeitpunkt 4 Generator Ladung (Bit 2)
constexpr uint16_t REG_TIME_POINT_5_GEN_CHARGE_ENABLE = 176;   // Zeitpunkt 5 Generator Ladung (Bit 2)
constexpr uint16_t REG_TIME_POINT_6_GEN_CHARGE_ENABLE = 177;   // Zeitpunkt 6 Generator Ladung (Bit 2)

// Weekday Enables (Register 146 - Time of Use register)
constexpr uint16_t REG_TIME_OF_USE_WEEKDAYS = 146;             // Wochentage Freigabe (Bits 1-7)
constexpr uint16_t BITMASK_WEEKDAY_MONDAY = 0x0002;            // Montag (Bit 1)
constexpr uint16_t BITMASK_WEEKDAY_TUESDAY = 0x0004;           // Dienstag (Bit 2)
constexpr uint16_t BITMASK_WEEKDAY_WEDNESDAY = 0x0008;         // Mittwoch (Bit 3)
constexpr uint16_t BITMASK_WEEKDAY_THURSDAY = 0x0010;          // Donnerstag (Bit 4)
constexpr uint16_t BITMASK_WEEKDAY_FRIDAY = 0x0020;            // Freitag (Bit 5)
constexpr uint16_t BITMASK_WEEKDAY_SATURDAY = 0x0040;          // Samstag (Bit 6)
constexpr uint16_t BITMASK_WEEKDAY_SUNDAY = 0x0080;            // Sonntag (Bit 7)

// Special Functions (178-184)
// Register 178 - Special Function 1: 6 functions with 2-bit values
// Bit 0-1: microinverter_export_to_grid (00/01=disabled, 10=disable, 11=enable)
// Bit 2-3: gen_peak_shaving (10=disable, 11=enable)
// Bit 4-5: grid_peak_shaving (10=disable, 11=enable)
// Bit 6-7: on_grid_always_on (10=disable, 11=enable)
// Bit 8-9: external_relay (10=disable, 11=disable) - special case
// Bit 10-11: battery_loss_report_fault (10=disable, 11=enable)
constexpr uint16_t REG_SPECIAL_FUNCTION_1 = 178;             // Spezialfunktionen 1

// Register 179 - Special Function 2: 2 functions with 2-bit values
// Bit 0-1: external_ct_direction_check (10=disable, 11=enable)
// Bit 2-3: forced_off_grid_work (10=disable, 11=enable)
constexpr uint16_t REG_SPECIAL_FUNCTION_2 = 179;             // Spezialfunktionen 2
constexpr uint16_t REG_RESTORE_CONNECTION_TIME = 180;        // Wiederverbindungszeit (s)
constexpr uint16_t REG_SOLAR_ARC_FAULT_MODE = 181;           // Solar Arc Fault Modus
constexpr uint16_t REG_GRID_MODE = 182;                      // Netz-Modus
constexpr uint16_t REG_GRID_NOMINAL_FREQUENCY = 183;         // Netz-Nennfrequenz
constexpr uint16_t REG_GRID_TYPE = 184;                      // Netz-Typ

// Battery Settings Range 2 (201-222)
constexpr uint16_t REG_EQ_VOLTAGE = 201;                     // Ausgleichsspannung (V)
constexpr uint16_t REG_ABS_VOLTAGE = 202;                    // Absorptionsspannung (V)
constexpr uint16_t REG_FLOAT_VOLTAGE_2 = 203;                // Float-Spannung (V)
constexpr uint16_t REG_BATTERY_CAPACITY_SETTING = 204;       // Batteriekapazität (Einstellung) (Ah)
constexpr uint16_t REG_BATTERY_EMPTY_VOLTAGE_2 = 205;        // Batterie-Leer-Spannung (V)
constexpr uint16_t REG_BATTERY_MIN_ZERO_EXPORT_SOC = 206;    // Batterie Min Zero-Export SOC (%)
constexpr uint16_t REG_BATTERY_EQUALIZATION_CYCLE = 207;     // Batterie-Ausgleichszyklus (Tage)
constexpr uint16_t REG_BATTERY_EQUALIZATION_DURATION = 208;  // Batterie-Ausgleichsdauer (h)
constexpr uint16_t REG_BATTERY_TEMP_COEFFICIENT = 209;       // Batterie-Temperaturkoeffizient (mV/°C)
constexpr uint16_t REG_MAX_BATTERY_CHARGE_CURRENT = 210;     // Maximaler Batterie-Ladestrom (A)
constexpr uint16_t REG_MAX_BATTERY_DISCHARGE_CURRENT = 211;  // Maximaler Batterie-Entladestrom (A)
constexpr uint16_t REG_DC5_CURRENT = 212;                    // DC5 Strom (A)
constexpr uint16_t REG_DC6_VOLTAGE = 213;                    // DC6 Spannung (V)
constexpr uint16_t REG_DC6_CURRENT = 214;                    // DC6 Strom (A)
constexpr uint16_t REG_DC7_VOLTAGE = 215;                    // DC7 Spannung (V)
constexpr uint16_t REG_DC7_CURRENT = 216;                    // DC7 Strom (A)
constexpr uint16_t REG_DC8_VOLTAGE = 217;                    // DC8 Spannung (V)
constexpr uint16_t REG_DC8_CURRENT = 218;                    // DC8 Strom (A)
constexpr uint16_t REG_RESERVE_219 = 219;                    // Reserve 219
constexpr uint16_t REG_BATTERY_SHUTDOWN_VOLTAGE_220 = 220;   // Batterie Abschaltspannung 220 (V)
constexpr uint16_t REG_BATTERY_RESTART_VOLTAGE_221 = 221;    // Batterie Neustartspannung 221 (V)
constexpr uint16_t REG_BATTERY_LOW_VOLTAGE_WARNING_222 = 222;// Batterie Niederspannungswarnung 222 (V)

// Generator Settings Range 2 (223-230)
constexpr uint16_t REG_GEN_MAX_TIME = 223;                   // Generator Max-Laufzeit (223) (h)
constexpr uint16_t REG_GEN_COOLDOWN = 224;                   // Generator Kühlzeit (224) (h)
constexpr uint16_t REG_GEN_START_VOLTAGE_225 = 225;          // Generator Start-Spannung (225) (V)
constexpr uint16_t REG_GEN_START_SOC_226 = 226;              // Generator Start-SOC (226) (%)
constexpr uint16_t REG_GEN_CHARGE_CURRENT_227 = 227;         // Generator Ladestrom (227) (A)
constexpr uint16_t REG_GRID_CHARGE_START_V = 228;            // Netz-Ladung Start-Spannung (V)
constexpr uint16_t REG_GRID_CHARGE_START_SOC = 229;          // Netz-Ladung Start-SOC (%)
constexpr uint16_t REG_GRID_CHARGE_CURRENT = 230;            // Netz-Ladestrom (A)

// Solar Settings (340)
constexpr uint16_t REG_MAX_SOLAR_POWER = 340;                // Max Solar-Leistung (W)

// =============================================================================
// STATUS REGISTERS (40 registers: 500, 548-585)
// =============================================================================

constexpr uint16_t REG_RUNNING_STATUS = 500;                         // Betriebsstatus
constexpr uint16_t REG_COMMUNICATION_BOARD_FAILURE_STATUS = 548;     // Kommunikationsplatine Fehlerstatus
constexpr uint16_t REG_RESERVE_549 = 549;                            // Reserve 549
constexpr uint16_t REG_RESERVE_550 = 550;                            // Reserve 550
constexpr uint16_t REG_TURN_OFF_ON_STATUS = 551;                     // Ein- und Ausschaltstatus
constexpr uint16_t REG_AC_INV_RELAY = 552;                           // AC Wechselrichter Relais
constexpr uint16_t REG_WARNING_1_RAW = 553;                          // Warnung 1 Raw
constexpr uint16_t REG_WARNING_2_RAW = 554;                          // Warnung 2 Raw
constexpr uint16_t REG_ERROR_1_RAW = 555;                            // Fehler 1 Raw
constexpr uint16_t REG_ERROR_2_RAW = 556;                            // Fehler 2 Raw
constexpr uint16_t REG_ERROR_3_RAW = 557;                            // Fehler 3 Raw
constexpr uint16_t REG_ERROR_4_RAW = 558;                            // Fehler 4 Raw
constexpr uint16_t REG_RESERVE_559 = 559;                            // Reserve 559
constexpr uint16_t REG_RESERVE_560 = 560;                            // Reserve 560
constexpr uint16_t REG_FAN_STATUS_561 = 561;                         // Lüfterstatus 561
constexpr uint16_t REG_FAN_STATUS_562 = 562;                         // Lüfterstatus 562
constexpr uint16_t REG_FAN_STATUS_563 = 563;                         // Lüfterstatus 563
constexpr uint16_t REG_FAN_STATUS_564 = 564;                         // Lüfterstatus 564
constexpr uint16_t REG_FAN_STATUS_565 = 565;                         // Lüfterstatus 565
constexpr uint16_t REG_FAN_STATUS_566 = 566;                         // Lüfterstatus 566
constexpr uint16_t REG_FAN_STATUS_567 = 567;                         // Lüfterstatus 567
constexpr uint16_t REG_FAN_STATUS_568 = 568;                         // Lüfterstatus 568
constexpr uint16_t REG_FAN_STATUS_569 = 569;                         // Lüfterstatus 569
constexpr uint16_t REG_FAN_STATUS_570 = 570;                         // Lüfterstatus 570
constexpr uint16_t REG_FAN_STATUS_571 = 571;                         // Lüfterstatus 571
constexpr uint16_t REG_FAN_STATUS_572 = 572;                         // Lüfterstatus 572
constexpr uint16_t REG_FAN_STATUS_573 = 573;                         // Lüfterstatus 573
constexpr uint16_t REG_FAN_STATUS_574 = 574;                         // Lüfterstatus 574
constexpr uint16_t REG_FAN_STATUS_575 = 575;                         // Lüfterstatus 575
constexpr uint16_t REG_FAN_STATUS_576 = 576;                         // Lüfterstatus 576
constexpr uint16_t REG_FAN_STATUS_577 = 577;                         // Lüfterstatus 577
constexpr uint16_t REG_FAN_STATUS_578 = 578;                         // Lüfterstatus 578
constexpr uint16_t REG_FAN_STATUS_579 = 579;                         // Lüfterstatus 579
constexpr uint16_t REG_FAN_STATUS_580 = 580;                         // Lüfterstatus 580
constexpr uint16_t REG_FAN_STATUS_581 = 581;                         // Lüfterstatus 581
constexpr uint16_t REG_FAN_STATUS_582 = 582;                         // Lüfterstatus 582
constexpr uint16_t REG_FAN_STATUS_583 = 583;                         // Lüfterstatus 583
constexpr uint16_t REG_RESERVE_584 = 584;                            // Reserve 584
constexpr uint16_t REG_RESERVE_585 = 585;                            // Reserve 585

// =============================================================================
// STATISTICS REGISTERS (39 registers: 501-539)
// =============================================================================

constexpr uint16_t REG_DAILY_ACTIVE_POWER_GENERATION = 501;      // Tägliche Wirkleistung (kWh)
constexpr uint16_t REG_ACTIVE_POWER_GENERATION_TODAY = 502;      // Heutige Wirkleistungserzeugung (kWh)
constexpr uint16_t REG_DAILY_GRID_CONNECTION_TIME = 503;         // Tägliche Netzanschlusszeit (min)
constexpr uint16_t REG_ACTIVE_POWER_GEN_TOTAL_LOW = 504;         // Aktive Energie Erzeugung Total Low (kWh)
constexpr uint16_t REG_ACTIVE_POWER_GEN_TOTAL_HIGH = 505;        // Aktive Energie Erzeugung Total High
constexpr uint16_t REG_REACTIVE_POWER_GEN_TOTAL_LOW = 506;       // Reaktive Energie Erzeugung Total Low
constexpr uint16_t REG_REACTIVE_POWER_GEN_TOTAL_HIGH = 507;      // Reaktive Energie Erzeugung Total High
constexpr uint16_t REG_RESERVE_508 = 508;                        // Reserve 508
constexpr uint16_t REG_RESERVE_509 = 509;                        // Reserve 509
constexpr uint16_t REG_RESERVE_510 = 510;                        // Reserve 510
constexpr uint16_t REG_RESERVE_511 = 511;                        // Reserve 511
constexpr uint16_t REG_RESERVE_512 = 512;                        // Reserve 512
constexpr uint16_t REG_RESERVE_513 = 513;                        // Reserve 513
constexpr uint16_t REG_DAILY_BATTERY_CHARGE = 514;               // Tägliche Batterie-Ladung (kWh)
constexpr uint16_t REG_DAILY_BATTERY_DISCHARGE = 515;            // Tägliche Batterie-Entladung (kWh)
constexpr uint16_t REG_TOTAL_BATTERY_CHARGE = 516;               // Gesamtladung der Batterie (kWh)
constexpr uint16_t REG_BATTERY_CHARGE_TOTAL_HIGH = 517;          // Batterie Ladung Total High (kWh)
constexpr uint16_t REG_TOTAL_BATTERY_DISCHARGE = 518;            // Gesamtentladung der Batterie (kWh)
constexpr uint16_t REG_BATTERY_DISCHARGE_TOTAL_HIGH = 519;       // Batterie Entladung Total High (kWh)
constexpr uint16_t REG_DAILY_ENERGY_BOUGHT = 520;                // Täglich gekaufte Energie (kWh)
constexpr uint16_t REG_DAILY_ENERGY_SOLD = 521;                  // Täglich verkaufte Energie (kWh)
constexpr uint16_t REG_TOTAL_ENERGY_BOUGHT = 522;                // Gesamt gekaufte Energie (kWh)
constexpr uint16_t REG_TOTAL_GRID_BUY_HIGH = 523;                // Total Grid Bezug High (kWh)
constexpr uint16_t REG_TOTAL_ENERGY_SOLD_524 = 524;              // Gesamt verkaufte Energie (kWh)
constexpr uint16_t REG_TOTAL_GRID_SELL_HIGH = 525;               // Total Grid Verkauf High (kWh)
constexpr uint16_t REG_DAILY_POWER_CONSUMPTION = 526;            // Täglicher Energieverbrauch (kWh)
constexpr uint16_t REG_TOTAL_CONSUMPTION = 527;                  // Gesamtverbrauch (kWh)
constexpr uint16_t REG_TOTAL_LOAD_HIGH = 528;                    // Total Last High (kWh)
constexpr uint16_t REG_DAILY_PRODUCTION = 529;                   // Tagesproduktion (kWh)
constexpr uint16_t REG_DAILY_PV1_PRODUCTION = 530;               // Tägliche PV1 Produktion (kWh)
constexpr uint16_t REG_DAILY_PV2_PRODUCTION = 531;               // Tägliche PV2 Produktion (kWh)
constexpr uint16_t REG_DAILY_PV3_PRODUCTION = 532;               // Tägliche PV3 Produktion (kWh)
constexpr uint16_t REG_DAILY_PV4_PRODUCTION = 533;               // Tägliche PV4 Produktion (kWh)
constexpr uint16_t REG_TOTAL_PV_PRODUCTION = 534;                // Gesamt PV-Erzeugung (kWh)
constexpr uint16_t REG_PV_RESERVE_535 = 535;                     // PV Reserve 535
constexpr uint16_t REG_RESERVE_536 = 536;                        // Reserve 536
constexpr uint16_t REG_RESERVE_537 = 537;                        // Reserve 537
constexpr uint16_t REG_RESERVE_538 = 538;                        // Reserve 538
constexpr uint16_t REG_DAILY_GENERATOR_ON_TIME = 539;            // Tägliche Generator-Laufzeit (h)

// =============================================================================
// LIVE DATA REGISTERS (110 registers: 540-541, 586-683)
// =============================================================================

// Temperatures (540-547)
constexpr uint16_t REG_DC_TRANSFORMER_TEMPERATURE = 540;         // DC Transformer Temperatur (°C)
constexpr uint16_t REG_HEAT_SINK_TEMPERATURE = 541;              // Kühlkörper-Temperatur (°C)
constexpr uint16_t REG_RESERVE_TEMPERATURE_1 = 542;              // Reserve Temperatur 1
constexpr uint16_t REG_RESERVE_TEMPERATURE_2 = 543;              // Reserve Temperatur 2
constexpr uint16_t REG_RESERVE_TEMPERATURE_3 = 544;              // Reserve Temperatur 3
constexpr uint16_t REG_RESERVE_545 = 545;                        // Reserve 545
constexpr uint16_t REG_RESERVE_546 = 546;                        // Reserve 546
constexpr uint16_t REG_RESERVE_547 = 547;                        // Reserve 547

// Battery Live Data (586-597)
constexpr uint16_t REG_BATTERY_TEMPERATURE = 586;                // Batterie Temperatur (°C)
constexpr uint16_t REG_BATTERY_VOLTAGE = 587;                    // Batteriespannung (V)
constexpr uint16_t REG_BATTERY_CAPACITY_LIVE = 588;              // Batteriekapazität (%)
constexpr uint16_t REG_RESERVE_589 = 589;                        // Reserve 589
constexpr uint16_t REG_BATTERY_POWER = 590;                      // Batterie-Ausgangsleistung (W)
constexpr uint16_t REG_BATTERY_CURRENT = 591;                    // Batterie-Ausgangsstrom (A)
constexpr uint16_t REG_BATTERY_CORRECTED_AH = 592;               // Batterie Korrigiert Ah
constexpr uint16_t REG_RESERVE_593 = 593;                        // Reserve 593
constexpr uint16_t REG_RESERVE_594 = 594;                        // Reserve 594
constexpr uint16_t REG_RESERVE_595 = 595;                        // Reserve 595
constexpr uint16_t REG_RESERVE_596 = 596;                        // Reserve 596
constexpr uint16_t REG_RESERVE_597 = 597;                        // Reserve 597

// Grid Port Live Data (598-612)
constexpr uint16_t REG_GRID_VOLTAGE_L1 = 598;                    // Netz-Spannung L1 (V)
constexpr uint16_t REG_GRID_VOLTAGE_L2 = 599;                    // Netz-Spannung L2 (V)
constexpr uint16_t REG_GRID_VOLTAGE_L3 = 600;                    // Netz-Spannung L3 (V)
constexpr uint16_t REG_GRID_VOLTAGE_L1_L2 = 601;                 // Netz Spannung L1-L2 (V)
constexpr uint16_t REG_GRID_VOLTAGE_L2_L3 = 602;                 // Netz Spannung L2-L3 (V)
constexpr uint16_t REG_GRID_VOLTAGE_L3_L1 = 603;                 // Netz Spannung L3-L1 (V)
constexpr uint16_t REG_INTERNAL_CT_L1_POWER = 604;               // Interne CT L1 Leistung (W)
constexpr uint16_t REG_INTERNAL_CT_L2_POWER = 605;               // Interne CT L2 Leistung (W)
constexpr uint16_t REG_INTERNAL_CT_L3_POWER = 606;               // Interne CT L3 Leistung (W)
constexpr uint16_t REG_INTERNAL_TOTAL_POWER = 607;               // Interne Gesamtleistung (W)
constexpr uint16_t REG_GRID_SIDE_TOTAL_APPARENT_POWER = 608;     // Grid Side Total Scheinleistung (VA)
constexpr uint16_t REG_GRID_FREQUENCY = 609;                     // Netzfrequenz (Hz)
constexpr uint16_t REG_GRID_SIDE_INNER_CURRENT_A = 610;          // Grid Side Inner Strom A (A)
constexpr uint16_t REG_GRID_SIDE_INNER_CURRENT_B = 611;          // Grid Side Inner Strom B (A)
constexpr uint16_t REG_GRID_SIDE_INNER_CURRENT_C = 612;          // Grid Side Inner Strom C (A)

// Grid Meter Live Data (613-626)
constexpr uint16_t REG_GRID_METER_CURRENT_L1 = 613;              // Grid Meter Strom L1 (A)
constexpr uint16_t REG_GRID_METER_CURRENT_L2 = 614;              // Grid Meter Strom L2 (A)
constexpr uint16_t REG_GRID_METER_CURRENT_L3 = 615;              // Grid Meter Strom L3 (A)
constexpr uint16_t REG_EXTERNAL_CT_L1_POWER = 616;               // Externe CT L1 Leistung (W)
constexpr uint16_t REG_EXTERNAL_CT_L2_POWER = 617;               // Externe CT L2 Leistung (W)
constexpr uint16_t REG_EXTERNAL_CT_L3_POWER = 618;               // Externe CT L3 Leistung (W)
constexpr uint16_t REG_OUT_OF_GRID_TOTAL_POWER = 619;            // Netzferne Gesamtleistung (W)
constexpr uint16_t REG_GRID_METER_APPARENT_POWER = 620;          // Grid Meter Scheinleistung (VA)
constexpr uint16_t REG_GRID_METER_POWER_FACTOR = 621;            // Grid Meter Leistungsfaktor
constexpr uint16_t REG_GRID_SIDE_A_PHASE_POWER = 622;            // Grid Side A Phase Leistung (W)
constexpr uint16_t REG_GRID_SIDE_B_PHASE_POWER = 623;            // Grid Side B Phase Leistung (W)
constexpr uint16_t REG_GRID_SIDE_C_PHASE_POWER = 624;            // Grid Side C Phase Leistung (W)
constexpr uint16_t REG_TOTAL_GRID_POWER = 625;                   // Gesamt Netz-Leistung (W)
constexpr uint16_t REG_GRID_SIDE_TOTAL_POWER = 626;              // Grid Side Gesamtleistung (W)

// Inverter Output Live Data (627-639)
constexpr uint16_t REG_INVERTER_VOLTAGE_L1 = 627;                // Wechselrichter Spannung L1 (V)
constexpr uint16_t REG_INVERTER_VOLTAGE_L2 = 628;                // Wechselrichter Spannung L2 (V)
constexpr uint16_t REG_INVERTER_VOLTAGE_L3 = 629;                // Wechselrichter Spannung L3 (V)
constexpr uint16_t REG_GRID_CURRENT_L1 = 630;                    // Netz Strom L1 (A)
constexpr uint16_t REG_GRID_CURRENT_L2 = 631;                    // Netz Strom L2 (A)
constexpr uint16_t REG_GRID_CURRENT_L3 = 632;                    // Netz Strom L3 (A)
constexpr uint16_t REG_INVERTER_REAL_POWER_L1 = 633;             // Wechselrichter Wirkleistung L1 (W)
constexpr uint16_t REG_INVERTER_REAL_POWER_L2 = 634;             // Wechselrichter Wirkleistung L2 (W)
constexpr uint16_t REG_INVERTER_REAL_POWER_L3 = 635;             // Wechselrichter Wirkleistung L3 (W)
constexpr uint16_t REG_INVERTER_REAL_POWER = 636;                // Wechselrichter Wirkleistung (W)
constexpr uint16_t REG_INVERTER_APPARENT_POWER = 637;            // Wechselrichter Scheinleistung (VA)
constexpr uint16_t REG_INVERTER_FREQUENCY = 638;                 // Wechselrichter-Frequenz (Hz)
constexpr uint16_t REG_INVERTER_FREQ_RESERVE = 639;              // Reserve 639

// UPS Load Live Data (640-643)
constexpr uint16_t REG_UPS_LOAD_POWER_L1 = 640;                  // UPS Last Leistung L1 (W)
constexpr uint16_t REG_UPS_LOAD_POWER_L2 = 641;                  // UPS Last Leistung L2 (W)
constexpr uint16_t REG_UPS_LOAD_POWER_L3 = 642;                  // UPS Last Leistung L3 (W)
constexpr uint16_t REG_UPS_LOAD_POWER_TOTAL = 643;               // UPS Last Leistung Total (W)

// Load Port (Grid Port) Live Data (644-660)
constexpr uint16_t REG_LOAD_PORT_VOLTAGE_L1 = 644;               // Last Port Spannung L1 (V)
constexpr uint16_t REG_LOAD_PORT_VOLTAGE_L2 = 645;               // Last Port Spannung L2 (V)
constexpr uint16_t REG_LOAD_PORT_VOLTAGE_L3 = 646;               // Last Port Spannung L3 (V)
constexpr uint16_t REG_LOAD_PORT_CURRENT_L1 = 647;               // Last Port Strom L1 (A)
constexpr uint16_t REG_LOAD_PORT_CURRENT_L2 = 648;               // Last Port Strom L2 (A)
constexpr uint16_t REG_LOAD_PORT_CURRENT_L3 = 649;               // Last Port Strom L3 (A)
constexpr uint16_t REG_LOAD_PORT_POWER_L1 = 650;                 // Last Port Leistung L1 (W)
constexpr uint16_t REG_LOAD_PORT_POWER_L2 = 651;                 // Last Port Leistung L2 (W)
constexpr uint16_t REG_LOAD_PORT_POWER_L3 = 652;                 // Last Port Leistung L3 (W)
constexpr uint16_t REG_LOAD_REAL_POWER = 653;                    // Last Wirkleistung (W)
constexpr uint16_t REG_LOAD_APPARENT_POWER = 654;                // Last Scheinleistung (VA)
constexpr uint16_t REG_LOAD_FREQUENCY = 655;                     // Last-Frequenz (Hz)
constexpr uint16_t REG_LOAD_FREQ_RESERVE_656 = 656;              // Reserve 656
constexpr uint16_t REG_LOAD_FREQ_RESERVE_657 = 657;              // Reserve 657
constexpr uint16_t REG_RESERVE_658 = 658;                        // Reserve 658
constexpr uint16_t REG_RESERVE_659 = 659;                        // Reserve 659
constexpr uint16_t REG_RESERVE_660 = 660;                        // Reserve 660

// Generator Port Live Data (661-671)
constexpr uint16_t REG_GEN_PORT_VOLTAGE_L1 = 661;                // Generator Port Spannung L1 (V)
constexpr uint16_t REG_GEN_PORT_VOLTAGE_L2 = 662;                // Generator Port Spannung L2 (V)
constexpr uint16_t REG_GEN_PORT_VOLTAGE_L3 = 663;                // Generator Port Spannung L3 (V)
constexpr uint16_t REG_GEN_PORT_POWER_L1 = 664;                  // Generator Port Leistung L1 (W)
constexpr uint16_t REG_GEN_PORT_POWER_L2 = 665;                  // Generator Port Leistung L2 (W)
constexpr uint16_t REG_GEN_PORT_POWER_L3 = 666;                  // Generator Port Leistung L3 (W)
constexpr uint16_t REG_GEN_PORT_POWER_TOTAL = 667;               // Generator Port Leistung Total (W)
constexpr uint16_t REG_GEN_PORT_CURRENT_L1 = 668;                // Generator Port Strom L1 (A)
constexpr uint16_t REG_GEN_PORT_CURRENT_L2 = 669;                // Generator Port Strom L2 (A)
constexpr uint16_t REG_GEN_PORT_CURRENT_L3 = 670;                // Generator Port Strom L3 (A)
constexpr uint16_t REG_GEN_PORT_FREQUENCY = 671;                 // Generator Port Frequenz (Hz)

// PV Live Data (672-683)
constexpr uint16_t REG_PV1_POWER = 672;                          // PV1 Leistung (W)
constexpr uint16_t REG_PV2_POWER = 673;                          // PV2 Leistung (W)
constexpr uint16_t REG_PV3_POWER = 674;                          // PV3 Leistung (W)
constexpr uint16_t REG_PV4_POWER = 675;                          // PV4 Leistung (W)
constexpr uint16_t REG_PV1_VOLTAGE = 676;                        // PV1 Spannung (V)
constexpr uint16_t REG_PV1_CURRENT = 677;                        // PV1 Strom (A)
constexpr uint16_t REG_PV2_VOLTAGE = 678;                        // PV2 Spannung (V)
constexpr uint16_t REG_PV2_CURRENT = 679;                        // PV2 Strom (A)
constexpr uint16_t REG_PV3_VOLTAGE = 680;                        // PV3 Spannung (V)
constexpr uint16_t REG_PV3_CURRENT = 681;                        // PV3 Strom (A)
constexpr uint16_t REG_PV4_VOLTAGE = 682;                        // PV4 Spannung (V)
constexpr uint16_t REG_PV4_CURRENT = 683;                        // PV4 Strom (A)

// =============================================================================
// BATTERY MODULE REGISTERS (124 registers: 684-809)
// =============================================================================

// Battery Module 1 (685-697)
constexpr uint16_t REG_BAT_MODULE_1_NUMBER = 685;           // Batteriemodul 1 Nummer
constexpr uint16_t REG_BAT_MODULE_1_TEMPERATURE = 686;      // Batteriemodul 1 Temperatur
constexpr uint16_t REG_BAT_MODULE_1_SOC = 687;              // Batteriemodul 1 SOC
constexpr uint16_t REG_BAT_MODULE_1_REMAIN_CAPACITY = 688;  // Batteriemodul 1 Restkapazität
constexpr uint16_t REG_BAT_MODULE_1_TOTAL_CAPACITY = 689;   // Batteriemodul 1 Gesamtkapazität
constexpr uint16_t REG_BAT_MODULE_1_CHARGE_1 = 690;         // Batteriemodul 1 Ladung 1
constexpr uint16_t REG_BAT_MODULE_1_CHARGE_2 = 691;         // Batteriemodul 1 Ladung 2
constexpr uint16_t REG_BAT_MODULE_1_DISCHARGE = 692;        // Batteriemodul 1 Entladung
constexpr uint16_t REG_BAT_MODULE_1_MAX_CELL_V = 693;       // Batteriemodul 1 Max Zellenspannung
constexpr uint16_t REG_BAT_MODULE_1_MIN_CELL_V = 694;       // Batteriemodul 1 Min Zellenspannung
constexpr uint16_t REG_BAT_MODULE_1_CYCLE = 695;            // Batteriemodul 1 Zyklen
constexpr uint16_t REG_BAT_MODULE_1_WARMING = 696;          // Batteriemodul 1 Aufwärmung
constexpr uint16_t REG_BAT_MODULE_1_FAULT = 697;            // Batteriemodul 1 Fehler

// Battery Module 2 (699-711)
constexpr uint16_t REG_BAT_MODULE_2_NUMBER = 699;           // Batteriemodul 2 Nummer
constexpr uint16_t REG_BAT_MODULE_2_TEMPERATURE = 700;      // Batteriemodul 2 Temperatur
constexpr uint16_t REG_BAT_MODULE_2_SOC = 701;              // Batteriemodul 2 SOC
constexpr uint16_t REG_BAT_MODULE_2_REMAIN_CAPACITY = 702;  // Batteriemodul 2 Restkapazität
constexpr uint16_t REG_BAT_MODULE_2_TOTAL_CAPACITY = 703;   // Batteriemodul 2 Gesamtkapazität
constexpr uint16_t REG_BAT_MODULE_2_CHARGE_1 = 704;         // Batteriemodul 2 Ladung 1
constexpr uint16_t REG_BAT_MODULE_2_CHARGE_2 = 705;         // Batteriemodul 2 Ladung 2
constexpr uint16_t REG_BAT_MODULE_2_DISCHARGE = 706;        // Batteriemodul 2 Entladung
constexpr uint16_t REG_BAT_MODULE_2_MAX_CELL_V = 707;       // Batteriemodul 2 Max Zellenspannung
constexpr uint16_t REG_BAT_MODULE_2_MIN_CELL_V = 708;       // Batteriemodul 2 Min Zellenspannung
constexpr uint16_t REG_BAT_MODULE_2_CYCLE = 709;            // Batteriemodul 2 Zyklen
constexpr uint16_t REG_BAT_MODULE_2_WARMING = 710;          // Batteriemodul 2 Aufwärmung
constexpr uint16_t REG_BAT_MODULE_2_FAULT = 711;            // Batteriemodul 2 Fehler

// Battery Module 3 (713-725)
constexpr uint16_t REG_BAT_MODULE_3_NUMBER = 713;           // Batteriemodul 3 Nummer
constexpr uint16_t REG_BAT_MODULE_3_TEMPERATURE = 714;      // Batteriemodul 3 Temperatur
constexpr uint16_t REG_BAT_MODULE_3_SOC = 715;              // Batteriemodul 3 SOC
constexpr uint16_t REG_BAT_MODULE_3_REMAIN_CAPACITY = 716;  // Batteriemodul 3 Restkapazität
constexpr uint16_t REG_BAT_MODULE_3_TOTAL_CAPACITY = 717;   // Batteriemodul 3 Gesamtkapazität
constexpr uint16_t REG_BAT_MODULE_3_CHARGE_1 = 718;         // Batteriemodul 3 Ladung 1
constexpr uint16_t REG_BAT_MODULE_3_CHARGE_2 = 719;         // Batteriemodul 3 Ladung 2
constexpr uint16_t REG_BAT_MODULE_3_DISCHARGE = 720;        // Batteriemodul 3 Entladung
constexpr uint16_t REG_BAT_MODULE_3_MAX_CELL_V = 721;       // Batteriemodul 3 Max Zellenspannung
constexpr uint16_t REG_BAT_MODULE_3_MIN_CELL_V = 722;       // Batteriemodul 3 Min Zellenspannung
constexpr uint16_t REG_BAT_MODULE_3_CYCLE = 723;            // Batteriemodul 3 Zyklen
constexpr uint16_t REG_BAT_MODULE_3_WARMING = 724;          // Batteriemodul 3 Aufwärmung
constexpr uint16_t REG_BAT_MODULE_3_FAULT = 725;            // Batteriemodul 3 Fehler

// Battery Module 4 (727-739)
constexpr uint16_t REG_BAT_MODULE_4_NUMBER = 727;           // Batteriemodul 4 Nummer
constexpr uint16_t REG_BAT_MODULE_4_TEMPERATURE = 728;      // Batteriemodul 4 Temperatur
constexpr uint16_t REG_BAT_MODULE_4_SOC = 729;              // Batteriemodul 4 SOC
constexpr uint16_t REG_BAT_MODULE_4_REMAIN_CAPACITY = 730;  // Batteriemodul 4 Restkapazität
constexpr uint16_t REG_BAT_MODULE_4_TOTAL_CAPACITY = 731;   // Batteriemodul 4 Gesamtkapazität
constexpr uint16_t REG_BAT_MODULE_4_CHARGE_1 = 732;         // Batteriemodul 4 Ladung 1
constexpr uint16_t REG_BAT_MODULE_4_CHARGE_2 = 733;         // Batteriemodul 4 Ladung 2
constexpr uint16_t REG_BAT_MODULE_4_DISCHARGE = 734;        // Batteriemodul 4 Entladung
constexpr uint16_t REG_BAT_MODULE_4_MAX_CELL_V = 735;       // Batteriemodul 4 Max Zellenspannung
constexpr uint16_t REG_BAT_MODULE_4_MIN_CELL_V = 736;       // Batteriemodul 4 Min Zellenspannung
constexpr uint16_t REG_BAT_MODULE_4_CYCLE = 737;            // Batteriemodul 4 Zyklen
constexpr uint16_t REG_BAT_MODULE_4_WARMING = 738;          // Batteriemodul 4 Aufwärmung
constexpr uint16_t REG_BAT_MODULE_4_FAULT = 739;            // Batteriemodul 4 Fehler

// Battery Module 5 (741-753)
constexpr uint16_t REG_BAT_MODULE_5_NUMBER = 741;           // Batteriemodul 5 Nummer
constexpr uint16_t REG_BAT_MODULE_5_TEMPERATURE = 742;      // Batteriemodul 5 Temperatur
constexpr uint16_t REG_BAT_MODULE_5_SOC = 743;              // Batteriemodul 5 SOC
constexpr uint16_t REG_BAT_MODULE_5_REMAIN_CAPACITY = 744;  // Batteriemodul 5 Restkapazität
constexpr uint16_t REG_BAT_MODULE_5_TOTAL_CAPACITY = 745;   // Batteriemodul 5 Gesamtkapazität
constexpr uint16_t REG_BAT_MODULE_5_CHARGE_1 = 746;         // Batteriemodul 5 Ladung 1
constexpr uint16_t REG_BAT_MODULE_5_CHARGE_2 = 747;         // Batteriemodul 5 Ladung 2
constexpr uint16_t REG_BAT_MODULE_5_DISCHARGE = 748;        // Batteriemodul 5 Entladung
constexpr uint16_t REG_BAT_MODULE_5_MAX_CELL_V = 749;       // Batteriemodul 5 Max Zellenspannung
constexpr uint16_t REG_BAT_MODULE_5_MIN_CELL_V = 750;       // Batteriemodul 5 Min Zellenspannung
constexpr uint16_t REG_BAT_MODULE_5_CYCLE = 751;            // Batteriemodul 5 Zyklen
constexpr uint16_t REG_BAT_MODULE_5_WARMING = 752;          // Batteriemodul 5 Aufwärmung
constexpr uint16_t REG_BAT_MODULE_5_FAULT = 753;            // Batteriemodul 5 Fehler

// Battery Module 6 (755-767)
constexpr uint16_t REG_BAT_MODULE_6_NUMBER = 755;           // Batteriemodul 6 Nummer
constexpr uint16_t REG_BAT_MODULE_6_TEMPERATURE = 756;      // Batteriemodul 6 Temperatur
constexpr uint16_t REG_BAT_MODULE_6_SOC = 757;              // Batteriemodul 6 SOC
constexpr uint16_t REG_BAT_MODULE_6_REMAIN_CAPACITY = 758;  // Batteriemodul 6 Restkapazität
constexpr uint16_t REG_BAT_MODULE_6_TOTAL_CAPACITY = 759;   // Batteriemodul 6 Gesamtkapazität
constexpr uint16_t REG_BAT_MODULE_6_CHARGE_1 = 760;         // Batteriemodul 6 Ladung 1
constexpr uint16_t REG_BAT_MODULE_6_CHARGE_2 = 761;         // Batteriemodul 6 Ladung 2
constexpr uint16_t REG_BAT_MODULE_6_DISCHARGE = 762;        // Batteriemodul 6 Entladung
constexpr uint16_t REG_BAT_MODULE_6_MAX_CELL_V = 763;       // Batteriemodul 6 Max Zellenspannung
constexpr uint16_t REG_BAT_MODULE_6_MIN_CELL_V = 764;       // Batteriemodul 6 Min Zellenspannung
constexpr uint16_t REG_BAT_MODULE_6_CYCLE = 765;            // Batteriemodul 6 Zyklen
constexpr uint16_t REG_BAT_MODULE_6_WARMING = 766;          // Batteriemodul 6 Aufwärmung
constexpr uint16_t REG_BAT_MODULE_6_FAULT = 767;            // Batteriemodul 6 Fehler

// Battery Module 7 (769-781)
constexpr uint16_t REG_BAT_MODULE_7_NUMBER = 769;           // Batteriemodul 7 Nummer
constexpr uint16_t REG_BAT_MODULE_7_TEMPERATURE = 770;      // Batteriemodul 7 Temperatur
constexpr uint16_t REG_BAT_MODULE_7_SOC = 771;              // Batteriemodul 7 SOC
constexpr uint16_t REG_BAT_MODULE_7_REMAIN_CAPACITY = 772;  // Batteriemodul 7 Restkapazität
constexpr uint16_t REG_BAT_MODULE_7_TOTAL_CAPACITY = 773;   // Batteriemodul 7 Gesamtkapazität
constexpr uint16_t REG_BAT_MODULE_7_CHARGE_1 = 774;         // Batteriemodul 7 Ladung 1
constexpr uint16_t REG_BAT_MODULE_7_CHARGE_2 = 775;         // Batteriemodul 7 Ladung 2
constexpr uint16_t REG_BAT_MODULE_7_DISCHARGE = 776;        // Batteriemodul 7 Entladung
constexpr uint16_t REG_BAT_MODULE_7_MAX_CELL_V = 777;       // Batteriemodul 7 Max Zellenspannung
constexpr uint16_t REG_BAT_MODULE_7_MIN_CELL_V = 778;       // Batteriemodul 7 Min Zellenspannung
constexpr uint16_t REG_BAT_MODULE_7_CYCLE = 779;            // Batteriemodul 7 Zyklen
constexpr uint16_t REG_BAT_MODULE_7_WARMING = 780;          // Batteriemodul 7 Aufwärmung
constexpr uint16_t REG_BAT_MODULE_7_FAULT = 781;            // Batteriemodul 7 Fehler

// Battery Module 8 (783-795)
constexpr uint16_t REG_BAT_MODULE_8_NUMBER = 783;           // Batteriemodul 8 Nummer
constexpr uint16_t REG_BAT_MODULE_8_TEMPERATURE = 784;      // Batteriemodul 8 Temperatur
constexpr uint16_t REG_BAT_MODULE_8_SOC = 785;              // Batteriemodul 8 SOC
constexpr uint16_t REG_BAT_MODULE_8_REMAIN_CAPACITY = 786;  // Batteriemodul 8 Restkapazität
constexpr uint16_t REG_BAT_MODULE_8_TOTAL_CAPACITY = 787;   // Batteriemodul 8 Gesamtkapazität
constexpr uint16_t REG_BAT_MODULE_8_CHARGE_1 = 788;         // Batteriemodul 8 Ladung 1
constexpr uint16_t REG_BAT_MODULE_8_CHARGE_2 = 789;         // Batteriemodul 8 Ladung 2
constexpr uint16_t REG_BAT_MODULE_8_DISCHARGE = 790;        // Batteriemodul 8 Entladung
constexpr uint16_t REG_BAT_MODULE_8_MAX_CELL_V = 791;       // Batteriemodul 8 Max Zellenspannung
constexpr uint16_t REG_BAT_MODULE_8_MIN_CELL_V = 792;       // Batteriemodul 8 Min Zellenspannung
constexpr uint16_t REG_BAT_MODULE_8_CYCLE = 793;            // Batteriemodul 8 Zyklen
constexpr uint16_t REG_BAT_MODULE_8_WARMING = 794;          // Batteriemodul 8 Aufwärmung
constexpr uint16_t REG_BAT_MODULE_8_FAULT = 795;            // Batteriemodul 8 Fehler

// Battery Module 9 (797-809)
constexpr uint16_t REG_BAT_MODULE_9_NUMBER = 797;           // Batteriemodul 9 Nummer
constexpr uint16_t REG_BAT_MODULE_9_TEMPERATURE = 798;      // Batteriemodul 9 Temperatur
constexpr uint16_t REG_BAT_MODULE_9_SOC = 799;              // Batteriemodul 9 SOC
constexpr uint16_t REG_BAT_MODULE_9_CAPACITY_PERCENT = 800; // Batteriemodul 9 Kapazität %
constexpr uint16_t REG_BAT_MODULE_9_TOTAL_CAPACITY = 801;   // Batteriemodul 9 Gesamtkapazität
constexpr uint16_t REG_BAT_MODULE_9_CHARGE_1 = 802;         // Batteriemodul 9 Ladung 1
constexpr uint16_t REG_BAT_MODULE_9_CHARGE_2 = 803;         // Batteriemodul 9 Ladung 2
constexpr uint16_t REG_BAT_MODULE_9_DISCHARGE = 804;        // Batteriemodul 9 Entladung
constexpr uint16_t REG_BAT_MODULE_9_MAX_CELL_V = 805;       // Batteriemodul 9 Max Zellenspannung
constexpr uint16_t REG_BAT_MODULE_9_MIN_CELL_V = 806;       // Batteriemodul 9 Min Zellenspannung
constexpr uint16_t REG_BAT_MODULE_9_CYCLE = 807;            // Batteriemodul 9 Zyklen
constexpr uint16_t REG_BAT_MODULE_9_WARMING = 808;          // Batteriemodul 9 Aufwärmung
constexpr uint16_t REG_BAT_MODULE_9_FAULT = 809;            // Batteriemodul 9 Fehler

// =============================================================================
// SPECIAL EXTENDED REGISTERS
// =============================================================================

constexpr uint16_t REG_SPECIAL_983 = 983;                   // Spezialregister 983
constexpr uint16_t REG_SPECIAL_1000 = 1000;                 // Spezialregister 1000 (0 Grad Referenz)
constexpr uint16_t REG_SPECIAL_1200 = 1200;                 // Spezialregister 1200 (20.0 Grad Referenz)
constexpr uint16_t REG_SPECIAL_1499 = 1499;                 // Spezialregister 1499

// =============================================================================
// REGISTER RANGES FOR OPTIMIZED READING
// =============================================================================

struct RegisterRange {
  uint16_t start;
  uint16_t count;
  const char* name;
};

// Device Info Ranges (boot-time read)
constexpr RegisterRange RANGE_DEVICE_INFO = {REG_DEVICE_TYPE, 2, "Device Info"};

// Settings Ranges (configuration, read periodically)
constexpr RegisterRange RANGE_BATTERY_SETTINGS_1 = {REG_BATTERY_TYPE, 23, "Battery Settings 1"};       // 98-120
constexpr RegisterRange RANGE_GENERATOR_SETTINGS_1 = {REG_GENERATOR_MAX_RUN_TIME, 7, "Generator Settings 1"}; // 121-127
constexpr RegisterRange RANGE_GRID_SETTINGS = {REG_MAX_BATTERY_GRID_CHARGE_CURRENT, 20, "Grid Settings"};     // 128-147
constexpr RegisterRange RANGE_TIME_POINT_START = {REG_TIME_POINT_1_START, 6, "Time Point Start"};      // 148-153
constexpr RegisterRange RANGE_TIME_POINT_POWER = {REG_TIME_POINT_1_POWER, 6, "Time Point Power"};      // 154-159
constexpr RegisterRange RANGE_TIME_POINT_VOLTAGE = {REG_TIME_POINT_1_MIN_VOLTAGE, 6, "Time Point Voltage"};   // 160-165
constexpr RegisterRange RANGE_TIME_POINT_CAPACITY = {REG_TIME_POINT_1_CAPACITY, 6, "Time Point Capacity"};    // 166-171
constexpr RegisterRange RANGE_TIME_POINT_CHARGE = {REG_TIME_POINT_1_CHARGE_ENABLE, 6, "Time Point Charge"};   // 172-177
constexpr RegisterRange RANGE_SPECIAL_FUNCTIONS = {REG_SPECIAL_FUNCTION_1, 7, "Special Functions"};    // 178-184
constexpr RegisterRange RANGE_BATTERY_SETTINGS_2 = {REG_EQ_VOLTAGE, 22, "Battery Settings 2"};         // 201-222
constexpr RegisterRange RANGE_GENERATOR_SETTINGS_2 = {REG_GEN_MAX_TIME, 8, "Generator Settings 2"};    // 223-230
constexpr RegisterRange RANGE_SOLAR_SETTINGS = {REG_MAX_SOLAR_POWER, 1, "Solar Settings"};             // 340

// Status Ranges (1-2s interval)
constexpr RegisterRange RANGE_RUNNING_STATUS = {REG_RUNNING_STATUS, 1, "Running Status"};              // 500
constexpr RegisterRange RANGE_COMM_STATUS = {REG_COMMUNICATION_BOARD_FAILURE_STATUS, 38, "Comm Status"}; // 548-585

// Statistics Ranges (5-10s interval)
constexpr RegisterRange RANGE_DAILY_STATS = {REG_DAILY_ACTIVE_POWER_GENERATION, 14, "Daily Stats"};    // 501-514
constexpr RegisterRange RANGE_BATTERY_STATS = {REG_DAILY_BATTERY_CHARGE, 6, "Battery Stats"};          // 514-519
constexpr RegisterRange RANGE_GRID_STATS = {REG_DAILY_ENERGY_BOUGHT, 10, "Grid Stats"};                // 520-529
constexpr RegisterRange RANGE_PV_STATS = {REG_DAILY_PRODUCTION, 11, "PV Stats"};                       // 529-539

// Live Data Ranges (1s interval - high frequency)
constexpr RegisterRange RANGE_TEMPERATURES = {REG_DC_TRANSFORMER_TEMPERATURE, 8, "Temperatures"};      // 540-547
constexpr RegisterRange RANGE_BATTERY_LIVE = {REG_BATTERY_TEMPERATURE, 12, "Battery Live"};            // 586-597
constexpr RegisterRange RANGE_GRID_PORT_LIVE = {REG_GRID_VOLTAGE_L1, 15, "Grid Port Live"};            // 598-612
constexpr RegisterRange RANGE_GRID_METER_LIVE = {REG_GRID_METER_CURRENT_L1, 14, "Grid Meter Live"};    // 613-626
constexpr RegisterRange RANGE_INVERTER_OUTPUT_LIVE = {REG_INVERTER_VOLTAGE_L1, 13, "Inverter Output Live"}; // 627-639
constexpr RegisterRange RANGE_UPS_LOAD_LIVE = {REG_UPS_LOAD_POWER_L1, 4, "UPS Load Live"};             // 640-643
constexpr RegisterRange RANGE_LOAD_PORT_LIVE = {REG_LOAD_PORT_VOLTAGE_L1, 17, "Load Port Live"};       // 644-660
constexpr RegisterRange RANGE_GENERATOR_PORT_LIVE = {REG_GEN_PORT_VOLTAGE_L1, 11, "Generator Port Live"};   // 661-671
constexpr RegisterRange RANGE_PV_LIVE = {REG_PV1_POWER, 12, "PV Live"};                                // 672-683

// Combined ranges for efficient bulk reading
constexpr RegisterRange RANGE_SETTINGS_BATTERY = {REG_BATTERY_TYPE, 37, "Settings Battery"};           // 98-134
constexpr RegisterRange RANGE_SETTINGS_SMART_LOAD = {REG_SMART_LOAD_OFF_VOLTAGE, 24, "Settings Smart Load"};  // 134-157
constexpr RegisterRange RANGE_SETTINGS_TIMEPOINTS_ALL = {REG_TIME_POINT_1_START, 30, "Settings Time Points All"}; // 148-177

// New Device Info Ranges
constexpr RegisterRange RANGE_DEVICE_INFO_EXTENDED = {REG_COMM_PROTOCOL_VERSION, 28, "Device Info Extended"};  // 2-29

// New Settings Ranges
constexpr RegisterRange RANGE_SYSTEM_SETTINGS = {REG_REMOTE_CONTROL_ENABLE, 38, "System Settings"};        // 60-97
constexpr RegisterRange RANGE_GRID_PROTECTION = {REG_GRID_OVERVOLTAGE_PROTECTION, 16, "Grid Protection"};  // 185-200
constexpr RegisterRange RANGE_EXTENDED_MONITORING = {REG_FACTORY_TEST_PROGRAM, 1, "Factory Test"};         // 240
constexpr RegisterRange RANGE_MONITORING_SETTINGS = {REG_GRID1_CURRENT, 21, "Monitoring Settings"};        // 269-289
constexpr RegisterRange RANGE_WIND_INPUT = {REG_SOLAR_AS_WIND_INPUT_ENABLE, 30, "Wind Input Settings"};    // 310-339
constexpr RegisterRange RANGE_CALIFORNIA_COMPLIANCE = {REG_RESERVED_341, 79, "California Compliance"};     // 341-419

// Battery Module Ranges (individual modules for selective reading)
constexpr RegisterRange RANGE_BATTERY_MODULE_1 = {REG_BAT_MODULE_1_NUMBER, 13, "Battery Module 1"};        // 685-697
constexpr RegisterRange RANGE_BATTERY_MODULE_2 = {REG_BAT_MODULE_2_NUMBER, 13, "Battery Module 2"};        // 699-711
constexpr RegisterRange RANGE_BATTERY_MODULE_3 = {REG_BAT_MODULE_3_NUMBER, 13, "Battery Module 3"};        // 713-725
constexpr RegisterRange RANGE_BATTERY_MODULE_4 = {REG_BAT_MODULE_4_NUMBER, 13, "Battery Module 4"};        // 727-739
constexpr RegisterRange RANGE_BATTERY_MODULE_5 = {REG_BAT_MODULE_5_NUMBER, 13, "Battery Module 5"};        // 741-753
constexpr RegisterRange RANGE_BATTERY_MODULE_6 = {REG_BAT_MODULE_6_NUMBER, 13, "Battery Module 6"};        // 755-767
constexpr RegisterRange RANGE_BATTERY_MODULE_7 = {REG_BAT_MODULE_7_NUMBER, 13, "Battery Module 7"};        // 769-781
constexpr RegisterRange RANGE_BATTERY_MODULE_8 = {REG_BAT_MODULE_8_NUMBER, 13, "Battery Module 8"};        // 783-795
constexpr RegisterRange RANGE_BATTERY_MODULE_9 = {REG_BAT_MODULE_9_NUMBER, 13, "Battery Module 9"};        // 797-809

// Combined Battery Module Range
constexpr RegisterRange RANGE_BATTERY_MODULES_ALL = {REG_BAT_MODULE_1_NUMBER, 125, "Battery Modules All"}; // 685-809

}  // namespace deye_inverter
}  // namespace esphome
