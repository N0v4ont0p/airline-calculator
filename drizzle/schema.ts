import { int, mysqlEnum, mysqlTable, text, timestamp, varchar } from "drizzle-orm/mysql-core";

/**
 * Core user table backing auth flow.
 * Extend this file with additional tables as your product grows.
 * Columns use camelCase to match both database fields and generated types.
 */
export const users = mysqlTable("users", {
  /**
   * Surrogate primary key. Auto-incremented numeric value managed by the database.
   * Use this for relations between tables.
   */
  id: int("id").autoincrement().primaryKey(),
  /** Manus OAuth identifier (openId) returned from the OAuth callback. Unique per user. */
  openId: varchar("openId", { length: 64 }).notNull().unique(),
  name: text("name"),
  email: varchar("email", { length: 320 }),
  loginMethod: varchar("loginMethod", { length: 64 }),
  role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  lastSignedIn: timestamp("lastSignedIn").defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;

/**
 * Saved routes - User's favorite flight routes for quick access
 */
export const savedRoutes = mysqlTable("saved_routes", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("user_id").notNull().references(() => users.id, { onDelete: "cascade" }),
  name: varchar("name", { length: 255 }),
  originIata: varchar("origin_iata", { length: 3 }).notNull(),
  destinationIata: varchar("destination_iata", { length: 3 }).notNull(),
  cabinClass: varchar("cabin_class", { length: 20 }),
  bookingClass: varchar("booking_class", { length: 2 }),
  eliteStatus: varchar("elite_status", { length: 20 }),
  ticketPrice: int("ticket_price"), // Store as cents to avoid decimal issues
  programs: text("programs"), // JSON array of program IDs
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().onUpdateNow().notNull(),
});

export type SavedRoute = typeof savedRoutes.$inferSelect;
export type InsertSavedRoute = typeof savedRoutes.$inferInsert;

/**
 * Calculation history - Track all calculations for analytics and user history
 */
export const calculationHistory = mysqlTable("calculation_history", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("user_id").references(() => users.id, { onDelete: "cascade" }),
  originIata: varchar("origin_iata", { length: 3 }).notNull(),
  destinationIata: varchar("destination_iata", { length: 3 }).notNull(),
  distanceNm: int("distance_nm").notNull(),
  cabinClass: varchar("cabin_class", { length: 20 }),
  bookingClass: varchar("booking_class", { length: 2 }),
  eliteStatus: varchar("elite_status", { length: 20 }),
  ticketPrice: int("ticket_price"), // Store as cents
  results: text("results").notNull(), // JSON with full calculation results
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export type CalculationHistory = typeof calculationHistory.$inferSelect;
export type InsertCalculationHistory = typeof calculationHistory.$inferInsert;

/**
 * Promotions - Active bonus offers from loyalty programs
 */
export const promotions = mysqlTable("promotions", {
  id: int("id").autoincrement().primaryKey(),
  programId: varchar("program_id", { length: 50 }).notNull(),
  title: varchar("title", { length: 255 }).notNull(),
  description: text("description"),
  bonusType: varchar("bonus_type", { length: 20 }), // 'percentage', 'fixed', 'multiplier'
  bonusValue: int("bonus_value"), // Store as integer (e.g., 50 for 50%)
  startDate: timestamp("start_date").notNull(),
  endDate: timestamp("end_date").notNull(),
  termsUrl: varchar("terms_url", { length: 500 }),
  isActive: int("is_active", { unsigned: true }).default(1).notNull(), // 1 = true, 0 = false
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export type Promotion = typeof promotions.$inferSelect;
export type InsertPromotion = typeof promotions.$inferInsert;

/**
 * Credit cards - Co-branded airline credit cards with bonus multipliers
 */
export const creditCards = mysqlTable("credit_cards", {
  id: int("id").autoincrement().primaryKey(),
  programId: varchar("program_id", { length: 50 }).notNull(),
  cardName: varchar("card_name", { length: 255 }).notNull(),
  issuer: varchar("issuer", { length: 100 }),
  bonusMultiplier: int("bonus_multiplier").notNull(), // e.g., 200 for 2x miles
  annualFee: int("annual_fee").notNull(), // Store as cents
  signupBonus: int("signup_bonus"), // Miles
  minSpend: int("min_spend"), // Store as cents
  cardUrl: varchar("card_url", { length: 500 }),
  isActive: int("is_active", { unsigned: true }).default(1).notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export type CreditCard = typeof creditCards.$inferSelect;
export type InsertCreditCard = typeof creditCards.$inferInsert;