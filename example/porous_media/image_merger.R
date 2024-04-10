setwd("~/GITHUB/LBM/biednie/TCLB")


library(png)

background = readPNG("example/ink/porous_media_contrast_1024x256.png")
graphics = readPNG("example/ink/SIGGRAPH_1024x256.png")

nx = dim(background)[2]
ny = dim(background)[1]

new_min = 0.01 +  1* min(background) # Define new minimum value
new_max = 0.99 * max(background)  # Define new maximum value
mix =  background 

scaled_mix = new_min + ((mix - min(mix)) * (new_max - new_min)) / (max(mix) - min(mix))

scaled_mix = background + graphics

#limit_max = 1
#scale = 10
#scaled_mix = scaled_mix / (1 + exp(scale * (scaled_mix - limit_max)))


# porosity = as.vector(scaled_mix[,,3])


porosity = as.vector(scaled_mix[,,3]) + as.vector(graphics[,,3])

###############3

# Convert the porosity vector back to a matrix form matching the original image dimensions
porosity_matrix = matrix(porosity, nrow = ny, ncol = nx, byrow = TRUE)

# Plot the porosity field
image(1:nx, 1:ny, porosity_matrix, col = terrain.colors(256), axes = FALSE, xlab = "", ylab = "")

# Add a color bar
# Define the color bar plot
color_bar <- function(color_vector, zlim=c(min(porosity), max(porosity))) {
  par(fig=c(0.91, 0.93, 0.2, 0.8), new=TRUE, mar=c(5, 4, 2, 2))
  plot(0, type='n', xlim=c(0, 1), ylim=zlim, xaxt='n', yaxt='n', xlab='', ylab='', main='')
  axis(4)
  abline(h = seq(zlim[1], zlim[2], length.out=length(color_vector)), col=color_vector, lwd=10)
}

# Add the color bar to the plot
color_bar(terrain.colors(256))