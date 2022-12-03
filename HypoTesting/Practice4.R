install.packages("MASS")
library(MASS)


attach(cats)
head(cats)

#Separate Male and Female
male <- subset(cats, subset=(cats$Sex=="M"))

Female<- subset(cats, subset=(cats$Sex=="F"))

MBwt<-male$Bwt
FBwt<-Female$Bwt

# Compute t-test
res <- t.test(first_sample, second_sample, var.equal = FALSE, conf.level = .95)
res

#P-value .0408 < .05

#################################################
##PART 2- PAIRED TEST
#################################################


first_sample<-c(4.6, 7.8, 9.1, 5.6, 6.9, 8.5, 5.3, 7.1, 3.2, 4.4)
second_sample<-c(6.6, 7.7, 9.0, 6.2, 7.8, 8.3, 5.9, 6.5, 5.8, 4.9)



res2<- t.test(first_sample, second_sample, paired = TRUE, alternative = "two.sided")
res2

res3<- t.test(first_sample, second_sample, paired = TRUE, alternative = "two.sided" , conf.level = .9)
res3