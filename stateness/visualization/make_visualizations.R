library(readxl)
library(dplyr)
library(ggplot2)


df <- read_excel("../../data/processed/stateness.xlsx")
df$approach <- case_when(
  df$approach == "lowest common denominator" ~ "Мінімальне",
  df$approach == "fully covered" ~ "Робоче",
  df$approach == "max definition" ~ "Максимальне",
)

df$approach <- as.character(df$approach)
df$approach <- factor(df$approach, levels=c("Мінімальне", "Робоче", "Максимальне"), ordered = TRUE)


binomial_dist <- df %>%
  ggplot(aes(y = successful_transition, x = stateness)) +
  geom_point() +
  geom_smooth(
    method = "glm", method.args = list(family = "binomial"), se = FALSE
    ) + 
  facet_wrap(~ approach) +
  theme_bw() +
  xlab("Потужність держави") + ylab("Успішність революції") +
  labs(
    title = "Потужність держави та успішність революцій",
    subtitle = "Згруповано за типом визначення потужності держави",
    caption = "Вихідний код можна знайти тут: https://github.com/hp0404/regimes-and-governance-project"
  )

ggsave(
  "../../reports/figures/binomial_dist.png", 
  plot = binomial_dist,
  dpi = 300)


df$successful_transition <- case_when(
  df$successful_transition == 1 ~ "Успіх",
  df$successful_transition == 0 ~ "Невдача",
)
df$successful_transition <- as.character(df$successful_transition)
df$successful_transition <- factor(df$successful_transition, levels=c("Невдача", "Успіх"), ordered = TRUE)


boxplots <- ggplot(df, aes(x = successful_transition, y = stateness, group=successful_transition)) +
  geom_boxplot() +
  facet_wrap(~ approach) +
  xlab("Успішність революції") + ylab("Потужність держави") +
  theme_bw() +
  #theme(text=element_text(size=16,  family="Garamond")) +
  labs(
    title = "Потужність держави та успішність революцій",
    subtitle = "Згруповано за типом визначення потужності держави",
    caption = "Вихідний код можна знайти тут: https://github.com/hp0404/regimes-and-governance-project"
    )

ggsave(
  "../../reports/figures/boxplots.png", 
  plot = boxplots,
  dpi = 300)

