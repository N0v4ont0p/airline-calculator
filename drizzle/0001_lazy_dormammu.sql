CREATE TABLE `calculation_history` (
	`id` int AUTO_INCREMENT NOT NULL,
	`user_id` int,
	`origin_iata` varchar(3) NOT NULL,
	`destination_iata` varchar(3) NOT NULL,
	`distance_nm` int NOT NULL,
	`cabin_class` varchar(20),
	`booking_class` varchar(2),
	`elite_status` varchar(20),
	`ticket_price` int,
	`results` text NOT NULL,
	`created_at` timestamp NOT NULL DEFAULT (now()),
	CONSTRAINT `calculation_history_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `credit_cards` (
	`id` int AUTO_INCREMENT NOT NULL,
	`program_id` varchar(50) NOT NULL,
	`card_name` varchar(255) NOT NULL,
	`issuer` varchar(100),
	`bonus_multiplier` int NOT NULL,
	`annual_fee` int NOT NULL,
	`signup_bonus` int,
	`min_spend` int,
	`card_url` varchar(500),
	`is_active` int unsigned NOT NULL DEFAULT 1,
	`created_at` timestamp NOT NULL DEFAULT (now()),
	CONSTRAINT `credit_cards_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `promotions` (
	`id` int AUTO_INCREMENT NOT NULL,
	`program_id` varchar(50) NOT NULL,
	`title` varchar(255) NOT NULL,
	`description` text,
	`bonus_type` varchar(20),
	`bonus_value` int,
	`start_date` timestamp NOT NULL,
	`end_date` timestamp NOT NULL,
	`terms_url` varchar(500),
	`is_active` int unsigned NOT NULL DEFAULT 1,
	`created_at` timestamp NOT NULL DEFAULT (now()),
	CONSTRAINT `promotions_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `saved_routes` (
	`id` int AUTO_INCREMENT NOT NULL,
	`user_id` int NOT NULL,
	`name` varchar(255),
	`origin_iata` varchar(3) NOT NULL,
	`destination_iata` varchar(3) NOT NULL,
	`cabin_class` varchar(20),
	`booking_class` varchar(2),
	`elite_status` varchar(20),
	`ticket_price` int,
	`programs` text,
	`created_at` timestamp NOT NULL DEFAULT (now()),
	`updated_at` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT `saved_routes_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
ALTER TABLE `calculation_history` ADD CONSTRAINT `calculation_history_user_id_users_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE `saved_routes` ADD CONSTRAINT `saved_routes_user_id_users_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE cascade ON UPDATE no action;